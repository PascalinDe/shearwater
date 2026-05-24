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
:synopsis: Main routine.
"""

# standard library imports
import time
import curses

# third party imports
# library specific imports
import shearwater.tui
import shearwater.tui.pprint
import shearwater.docker
import shearwater.docker.system
import shearwater.docker.containers


def loop(stdscr):
    """Loop through Docker engine API calls.

    :param window stdscr: initial window
    """
    tui = shearwater.tui.TUI(stdscr)
    all_ = False
    limit = -1
    size = False
    while True:
        ch = stdscr.getch()
        tui.stdscr.erase()
        if ord("a") == ch:
            all_ = not all_
        if ord("l") == ch:
            limit = shearwater.tui.textbox(
                "Enter limit",
                tui.tabs["containers"],
                1,
                2,
                int,
            )
        if ord("s") == ch:
            size = not size
        try:
            body = shearwater.docker.system.version()
        except shearwater.docker.APICallFailed as exception:
            shearwater.tui.addstrs(
                tui.header,
                shearwater.tui.pprint.pprint_error(str(exception)),
            )
            continue
        strs = shearwater.tui.pprint.pprint_version(body)
        strs += shearwater.tui.pprint.pprint_tabs(
            ["Containers"],
            0,
            y=shearwater.tui.NLINES_VERSION - 1,
        )
        shearwater.tui.addstrs(tui.header, strs)
        for tab in tui.tabs:
            try:
                if tab.type == "containers":
                    body = shearwater.docker.containers.list_containers(
                        all_=all_,
                        limit=limit if not all_ else -1,
                        size=size,
                    )
            except shearwater.docker.APICallFailed as exception:
                shearwater.tui.addstrs(
                    tab.subwin,
                    shearwater.tui.pprint.pprint_error(str(exception)),
                )
                continue
            if tab.type == "containers":
                strs = shearwater.tui.pprint.pprint_containers(
                    body,
                    tab.subwin.getmaxyx()[1],
                )
            shearwater.tui.addstrs(tab.subwin, strs)
        tui.stdscr.refresh()
        time.sleep(1)


def main():
    """Main routine."""
    curses.wrapper(loop)
