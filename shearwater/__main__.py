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
    pads = {
        shearwater.docker.VERSION: stdscr.subpad(0, 0),
        shearwater.docker.DF: stdscr.subpad(shearwater.tui.NLINES_VERSION, 0),
    }
    shearwater.tui.init()
    while True:
        for path, pad in pads.items():
            try:
                body = shearwater.docker.call_api(path)
            except shearwater.docker.APICallFailed as exception:
                shearwater.tui.addstrs(
                    pad,
                    shearwater.tui.pprint_error(str(exception)),
                )
                continue
            pprint = {
                shearwater.docker.VERSION: shearwater.tui.pprint_version,
                shearwater.docker.DF: shearwater.tui.pprint_df,
            }[path]
            shearwater.tui.addstrs(pad, pprint(body))
        time.sleep(1)


def main():
    """Main routine."""
    curses.wrapper(loop)
