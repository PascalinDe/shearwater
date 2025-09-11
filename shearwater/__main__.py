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
import shearwater.docker


def loop(stdscr):
    """Loop through Docker engine API calls.

    :param window stdscr: initial window
    """
    main_win = curses.newwin(*stdscr.getmaxyx(), 0, 0)
    pads = {
        shearwater.docker.VERSION: main_win.subpad(0, 0),
        shearwater.docker.CONTAINERS: main_win.subpad(
            shearwater.tui.NLINES_VERSION,
            0,
        ),
    }
    shearwater.tui.init()
    while True:
        main_win.erase()
        for path, pad in pads.items():
            try:
                if path == shearwater.docker.CONTAINERS:
                    body = shearwater.docker.call_list_containers()
                else:
                    body = shearwater.docker.call_api(path)
            except shearwater.docker.APICallFailed as exception:
                shearwater.tui.addstrs(
                    pad,
                    shearwater.tui.pprint_error(str(exception)),
                )
                continue
            if path == shearwater.docker.VERSION:
                strs = shearwater.tui.pprint_version(body)
            if path == shearwater.docker.CONTAINERS:
                strs = shearwater.tui.pprint_containers(
                    body,
                    pad.getmaxyx()[1],
                )
            shearwater.tui.addstrs(pad, strs)
        main_win.refresh()
        time.sleep(1)


def main():
    """Main routine."""
    curses.wrapper(loop)
