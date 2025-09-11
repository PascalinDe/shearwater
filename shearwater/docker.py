#    This file is part of Shearwater.
#    Copyright (C) 2025  Carine Dengler
#
#    Shearwater is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
:synopsis: Docker API.
"""


# standard library imports
import os
import json
import select
import socket
import email.parser

from collections import defaultdict

# third party imports
# library specific imports


# https://github.com/python/cpython/blob/1a07a01014bde23acd2684916ef38dc0cd73c2de/Lib/multiprocessing/connection.py#L42
HOST = "localhost"
# https://www.rfc-editor.org/rfc/rfc2616#section-2.2
CR_LF = b"\r\n"


DOCKER_DAEMON_SOCKET = "/var/run/docker.sock"
API_VERSION = "/v1.49"

# containers API
CONTAINERS = f"{API_VERSION}/containers/json"
# system API
INFO = f"{API_VERSION}/info"
VERSION = f"{API_VERSION}/version"
EVENTS = f"{API_VERSION}/events"
DF = f"{API_VERSION}/system/df"


class APICallFailed(Exception):
    """Raised when Docker API call failed."""
    pass


def readfile(fp):
    """Read file object associated with the socket.

    :param fp: file object

    :returns: HTTP response
    :rtype: bytes
    """
    response = []
    chunked_transfer = False
    # read start line
    while True:
        line = fp.readline()
        if not line:
            return b"".join(response)
        response.append(line)
        if line == CR_LF:
            break
        protocol, status_code, _ = line.split(b" ", maxsplit=2)
        if protocol != b"HTTP/1.1":
            raise NotImplementedError
        break
    # read headers
    while True:
        line = fp.readline()
        if not line:
            return b"".join(response)
        response.append(line)
        if line == CR_LF:
            break
        name, value = line.split(b":", 1)
        value = value.strip()
        chunked_transfer = (
            name == b"Transfer-Encoding"
            and value == b"chunked"
        )
    # read body
    if chunked_transfer:
        while True:
            line = fp.readline()
            if not line:
                return b"".join(response)
            try:
                chunk_size = int(line, base=16)
            except ValueError:
                continue
            line = fp.readline()
            if not line:
                return b"".join(response)
            response.append(
                line[:chunk_size] if chunk_size > 0 else line
            )
            if chunk_size == 0:
                break
        # read trailer
        while True:
            line = fp.readline()
            if not line:
                return b"".join(response)
            response.append(line)
    if not chunked_transfer:
        while True:
            line = fp.readline()
            if not line:
                return b"".join(response)
            response.append(line)


def send(path):
    """Send HTTP request on Docker daemon socket.

    :param str path: path

    :returns: HTTP response
    :rtype: bytes
    """
    request = f"GET {path} HTTP/1.1{os.linesep}Host: {HOST}{2 * os.linesep}".encode()   # noqa: E501
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.setblocking(False)
        sock.connect(DOCKER_DAEMON_SOCKET)
        _, wsock, _ = select.select([], [sock], [])
        wsock[0].sendall(request)
        rsock, _, _ = select.select([sock], [], [])
        with rsock[0].makefile(mode="rb", newline=CR_LF) as fp:
            return readfile(fp)


def parse_http_response(response):
    """Parse HTTP response.

    :param bytes response: HTTP response

    :returns: HTTP response
    :rtype: dict
    """
    start_line, response = response.split(CR_LF, 1)
    headers, response = response.split(2 * CR_LF, 1)
    try:
        body, additional_headers = response.split(2 * CR_LF, 1)
        headers = additional_headers
    except ValueError:
        body = response
    body = body.replace(CR_LF, b"").decode()
    body = json.loads(body) if body else {}
    headers = dict(
        email.parser.BytesHeaderParser().parsebytes(headers).items()
    )
    return {
        "start_line": start_line.decode(),
        "headers": headers,
        "body": body,
    }


def call_api(path):
    """Call Docker engine API.

    :param str path: path

    :raises APICallFailed: if Docker engine API call failed

    :returns: HTTP response body
    :rtype: dict
    """
    try:
        response = parse_http_response(send(path))
    except Exception as exception:
        raise APICallFailed("Docker engine API call failed") from exception
    status_code = response["start_line"].split(" ")[1]
    if not status_code == "200":
        raise APICallFailed(f"{status_code} {response['body']['message']}")
    return response["body"]


def _convert_camel_to_snake(camel_str):
    """Convert camel case to snake case.

    :param str camel_str: camel-case string

    :returns: snake-case string
    :rtype: str
    """
    # acronyms should just be converted to lower case
    if all((c.isupper() for c in camel_str)):
        return camel_str.lower()
    return "".join(
        f"_{c.lower()}" if c.isupper() and i != 0 else c.lower()
        for i, c in enumerate(camel_str)
    )


def call_list_containers():
    """Call list containers API.

    :returns: list of containers
    :rtype: dict
    """
    body = call_api(CONTAINERS)
    containers = defaultdict(dict)
    for container in body:
        id_ = container["Id"]
        for key in (
                "Image",
                "Command",
                "Created",
                "Status",
                "Ports",
                "Names",
        ):
            if key not in ("Ports", "Names"):
                containers[id_][_convert_camel_to_snake(key)] = container[key]
            if key == "Ports":
                containers[id_][_convert_camel_to_snake(key)] = [
                    {
                        _convert_camel_to_snake(k): port.get(k, "")
                        for k in ("IP", "PrivatePort", "PublicPort", "Type")
                    } for port in container["Ports"]
                ]
            if key == "Names":
                containers[id_][_convert_camel_to_snake(key)] = [
                    name.strip("/") for name in container[key]
                ]
    return containers


def call_version():
    """Call version API.

    :returns: version
    :rtype: dict
    """
    body = call_api(VERSION)
    version = {}
    for k in ("Platform", "Version", "ApiVersion"):
        if k == "Platform":
            version[_convert_camel_to_snake(k)] = {
                _convert_camel_to_snake("Name"): body["Platform"]["Name"]
            }
        else:
            version[_convert_camel_to_snake(k)] = body[k]
    return version
