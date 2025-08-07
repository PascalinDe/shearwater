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
:synopsis: Text-based user interface.
"""


# standard library imports
import curses

# third party imports
# library specific imports


def pprint_version(version, y=0, x=0):
    """Pretty-print version of Docker.

    :param dict version: version of Docker and information about the system
    :param int y: Y-coordinate
    :param int x: X-coordinate

    :returns: pretty-printed version of Docker
    :rtype: list
    """
    strs = []
    for i, item in enumerate(
        (
            ("Platform:", version["Platform"]["Name"]),
            ("Docker daemon version:", version["Version"]),
            ("Docker engine API version:", version["ApiVersion"]),
        )
    ):
        strs.append((y + i, x + 0, item[0], curses.color_pair(6)))
        strs.append(
            (
                y + i,
                x + len(item[0]) + 1,
                item[1],
                curses.color_pair(6) | curses.A_BOLD
            ),
        )
    return strs


def pprint_df(df, y=0, x=0):
    """Pretty-print data usage information.

    :param dict df: data usage information
    :param int y: Y-coordinate
    :param int x: X-coordinate

    :returns: pretty-printed data usage information
    :rtype: list
    """
    strs = [
        (
            y + 0,
            x + 0,
            "CONTAINER ID\tIMAGE\tCOMMAND\tCREATED\tSTATUS\tPORTS\tNAMES",
            curses.color_pair(8),
        ),
    ]
    for i, container in enumerate(
            sorted(df["Containers"], key=lambda container: container["State"]),
            start=1,
    ):
        pprinted_ports = []
        for port in container["Ports"]:
            pprinted_ip = port.get("IP", "")
            pprinted_private_port = port["PrivatePort"]
            pprinted_public_port = port.get("PublicPort", "")
            pprinted_type = port["Type"]
            pprinted_port = f"{pprinted_private_port}/{pprinted_type}"
            if pprinted_public_port:
                pprinted_port = f"{pprinted_public_port}->" + pprinted_port
            if pprinted_ip:
                pprinted_port = f"{pprinted_ip}:" + pprinted_port
            pprinted_ports.append(pprinted_port)
        strs.append(
            (
                y + i,
                x + 0,
                f"{container['Id'][:12]}\t{container['Image']}\t{container['Command']}\t{container['Created']}\t{container['Status']}\t{', '.join(pprinted_ports)}\t{','.join(container['Names'])}", curses.color_pair(7),  # noqa: E501
            ),
        )
    return strs


def pprint_error(status_code, message, y=0, x=0):
    """Pretty-print HTTP error response.

    :param str status_code: HTTP reponse status code
    :param str message: HTTP message
    :param int y: Y-coordinate
    :param int x: X-coordinate

    :returns: pretty-printed HTTP error response
    :rtype: list
    """
    return [
        (
            y + 0,
            x + 0,
            f"{status_code} {message}",
            curses.color_pair(1) | curses.A_BOLD,
        )
    ]


def addstrs(window, strs):
    """Paint the character strings strs.

    :param window window: window
    :param list strs: character strings
    """
    window.erase()
    for y, x, str_, attr in strs:
        window.addstr(y, x, str_, attr)
    window.refresh()


def init():
    """Initialise text-based user interface."""
    curses.use_default_colors()
    # initialise default colours
    # COLOR_BLACK   0
    # COLOR_RED     1
    # COLOR_GREEN   2
    # COLOR_YELLOW  3
    # COLOR_BLUE    4
    # COLOR_MAGENTA 5
    # COLOR_CYAN    6
    # COLOR_WHITE   7
    for i in range(0, 8):
        curses.init_pair(i, i, -1)
    curses.init_pair(8, 0, curses.COLOR_GREEN)
