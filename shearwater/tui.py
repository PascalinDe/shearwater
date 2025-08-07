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


def pprint_version(version):
    """Pretty-print version of Docker.

    :param dict version: version of Docker and information about the system

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
        strs.append((i, 0, item[0], curses.color_pair(6)))
        strs.append(
            (
                i,
                len(item[0]) + 1,
                item[1],
                curses.color_pair(6) | curses.A_BOLD
            ),
        )
    return strs


def pprint_error(status_code, message):
    """Pretty-print HTTP error response.

    :param str status_code: HTTP reponse status code
    :param str message: HTTP message

    :returns: pretty-printed HTTP error response
    :rtype: list
    """
    return [
        (
            0,
            0,
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
