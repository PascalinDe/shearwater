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
import datetime

# third party imports
# library specific imports


NLINES_VERSION = 3


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
            ("Platform:", version["platform"]["name"]),
            ("Docker daemon version:", version["version"]),
            ("Docker engine API version:", version["api_version"]),
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


def pprint_containers(containers, max_x, y=0, x=0):
    """Pretty-print list of containers.

    :param dict containers: list of containers
    :param int max_x: maximum X-coordinate
    :param int y: Y-coordinate
    :param int x: X-coordinate

    :returns: pretty-printed data usage information
    :rtype: list
    """
    headers = (
        "CONTAINER ID",
        "IMAGE",
        "COMMAND",
        "CREATED",
        "STATUS",
        "PORTS",
        "NAMES",
    )
    num_chars = max_x // len(headers)
    r = max_x - len(headers) * num_chars
    strs = [
        (
            y,
            x + i * num_chars,
            f"{header:{num_chars if i < len(headers) - 1 else num_chars + r}}",
            curses.color_pair(8),
        )
        for i, header in enumerate(headers)
    ]
    for i, (id_, container) in enumerate(
        containers.items(),
        start=1,
    ):
        strs.append(
            (
                y + i,
                x,
                id_[:min(12, num_chars - 1)],
                curses.color_pair(7),
            ),
        )
        for j, k in enumerate(container.keys(), start=1):
            if k == "created":
                delta = (
                    datetime.datetime.now()
                    - datetime.datetime.fromtimestamp(container["created"])
                )
                seconds = int(
                    delta.total_seconds()
                )   # truncate to 'seconds' unit
                for unit, divisor in (
                        ("weeks", 60 * 60 * 24 * 7),
                        ("days", 60 * 60 * 24),
                        ("hours", 60 * 60),
                        ("minutes", 60),
                        ("seconds", 1),
                ):
                    value = seconds // divisor
                    if value:
                        pprinted_created = f"{value} {unit} ago"
                        created = (
                            y + i,
                            x + j * num_chars,
                            pprinted_created[
                                :min(len(pprinted_created), num_chars - 1)
                            ],
                            curses.color_pair(7),
                        )
                        break   # use biggest unit
                strs.append(created)
                continue
            if k == "ports":
                pprinted_ports = ""
                for port in container["ports"]:
                    pprinted_port = f"{port['private_port']}/{port['type']}"
                    if port["public_port"]:
                        pprinted_port = (
                            f"{port['public_port']}->"
                            + pprinted_port
                        )
                    if port["ip"]:
                        pprinted_port = (
                            f"{port['ip']}:"
                            + pprinted_port
                        )
                    pprinted_ports = (
                        pprinted_ports + f", {pprinted_port}"
                        if pprinted_ports else pprinted_port
                    )
                strs.append(
                    (
                        y + i,
                        x + j * num_chars,
                        pprinted_ports[
                            :min(len(pprinted_ports), num_chars - 1)
                        ],
                        curses.color_pair(7),
                    ),
                )
                continue
            if k == "names":
                pprinted_names = ",".join(container["names"])
                strs.append(
                    (
                        y + i,
                        x + j * num_chars,
                        pprinted_names[
                            :min(len(pprinted_names), num_chars - 1)
                        ],
                        curses.color_pair(7),
                    ),
                )
                continue
            else:
                strs.append(
                    (
                        y + i,
                        x + j * num_chars,
                        container[k][:min(len(container[k]), num_chars - 1)],
                        curses.color_pair(7),
                    ),
                )
    return strs


def pprint_error(message, y=0, x=0):
    """Pretty-print error message.

    :param str message: error message
    :param int y: Y-coordinate
    :param int x: X-coordinate

    :returns: pretty-printed error message
    :rtype: list
    """
    return [
        (
            y + 0,
            x + 0,
            message,
            curses.color_pair(1) | curses.A_BOLD,
        )
    ]


def addstrs(window, strs):
    """Paint the character strings strs.

    :param window window: window
    :param list strs: character strings
    """
    for y, x, str_, attr in strs:
        try:
            window.addstr(y, x, str_, attr)
        except TypeError:
            raise SystemExit(str_)


def init():
    """Initialise NCURSES."""
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


class TUI:
    """Text-based user interface."""

    def __init__(self, stdscr):
        """Initialise text-based user interface.

        :param window stdscr: initial window
        """
        self.scr = {
            "std": stdscr,
            "version": stdscr.subwin(0, 0),
            "containers": stdscr.subwin(NLINES_VERSION, 0),
        }
        init()
