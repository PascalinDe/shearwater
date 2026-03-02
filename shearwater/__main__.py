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
    tui = shearwater.tui.TUI(stdscr)
    while True:
        tui.scr["std"].erase()
        stdscr.erase()
        for type_, subwin in tui.scr.items():
            if type_ == "std":
                continue
            try:
                if type_ == "containers":
                    body = shearwater.docker.call_list_containers()
                else:
                    body = shearwater.docker.call_version()
            except shearwater.docker.APICallFailed as exception:
                shearwater.tui.addstrs(
                    subwin,
                    shearwater.tui.pprint_error(str(exception)),
                )
                continue
            if type_ == "version":
                strs = shearwater.tui.pprint_version(body)
            if type_ == "containers":
                strs = shearwater.tui.pprint_containers(
                    body,
                    subwin.getmaxyx()[1],
                )
            shearwater.tui.addstrs(subwin, strs)
        tui.scr["std"].refresh()
        time.sleep(1)


def main():
    """Main routine."""
    curses.wrapper(loop)
