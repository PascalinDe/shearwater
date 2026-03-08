#    This file is part of Shearwater.
#    Copyright (C) 2026  Carine Dengler
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
:synopsis: Docker Containers API.
"""

# standard library imports
import collections

# third party imports
# library specific imports
import shearwater.docker

CONTAINERS = f"{shearwater.docker.API_VERSION}/containers/json"


def call_list_containers(all_=True):
    """Call list containers API.

    :param bool all: toggle returning all containers on/off

    :returns: list of containers
    :rtype: dict
    """
    body = shearwater.docker.call_api(CONTAINERS, all=all_)
    containers = collections.defaultdict(dict)
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
                containers[id_][shearwater.docker._convert_camel_to_snake(key)] = (
                    container[key]
                )
            if key == "Ports":
                containers[id_][shearwater.docker._convert_camel_to_snake(key)] = [
                    {
                        shearwater.docker._convert_camel_to_snake(k): port.get(k, "")
                        for k in ("IP", "PrivatePort", "PublicPort", "Type")
                    }
                    for port in container["Ports"]
                ]
            if key == "Names":
                containers[id_][shearwater.docker._convert_camel_to_snake(key)] = [
                    name.strip("/") for name in container[key]
                ]
    return containers
