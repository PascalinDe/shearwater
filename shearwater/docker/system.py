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
:synopsis: Docker System API.
"""

# standard library imports
# third party imports
# library specific imports
import shearwater.docker

VERSION = f"{shearwater.docker.API_VERSION}/version"


def call_version():
    """Call version API.

    :returns: version
    :rtype: dict
    """
    body = shearwater.docker.call_api(VERSION)
    version = {}
    for k in ("Platform", "Version", "ApiVersion"):
        if k == "Platform":
            version[shearwater.docker._convert_camel_to_snake(k)] = {
                shearwater.docker._convert_camel_to_snake("Name"): body["Platform"][
                    "Name"
                ]
            }
        else:
            version[shearwater.docker._convert_camel_to_snake(k)] = body[k]
    return version
