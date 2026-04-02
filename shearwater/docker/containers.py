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
import json
import collections

# third party imports
# library specific imports
import shearwater.docker

CONTAINERS = f"{shearwater.docker.API_VERSION}/containers/json"


def call_list_containers(all_=False, limit=-1, size=False, **filters):
    """Call list containers API.

    :param bool all: toggle returning all containers on/off
    :param int limit: return n most recently created containers
    :param bool size: toggle returning the size of containers on/off
    :param dict filters: filters to process on the container list

    :returns: list of containers
    :rtype: dict
    """
    parameters = {
        "all": all_,
        "size": size,
        "filters": json.dumps(filters),
    }
    if limit > -1:
        parameters["limit"] = limit
    body = shearwater.docker.call_api(CONTAINERS, **parameters)
    containers = collections.defaultdict(dict)
    keys = (
        "Image",
        "Command",
        "Created",
        "Status",
        "Ports",
        "Names",
    )
    if size:
        keys = (
            *keys,
            "SizeRw",
            "SizeRootFs",
        )
    for container in body:
        id_ = container["Id"]
        size = {}
        for key in keys:
            if key not in keys[-4:]:
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
            if key in ("SizeRw", "SizeRootFs"):
                size[shearwater.docker._convert_camel_to_snake(key)] = container[key]
        if size:
            containers[id_]["size"] = size
    return containers
