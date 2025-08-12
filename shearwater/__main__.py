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
    shearwater.tui.init()
    while True:
        strs = []
        for path in (shearwater.docker.VERSION, shearwater.docker.DF):
            y = strs[-1][0] + 1 if strs else 0
            try:
                body = shearwater.docker.call_api(path)
            except shearwater.docker.APICallFailed as exception:
                strs += shearwater.tui.pprint_error(str(exception), y=y)
            else:
                pprint = {
                    shearwater.docker.VERSION: shearwater.tui.pprint_version,
                    shearwater.docker.DF: shearwater.tui.pprint_df,
                }[path]
                strs += pprint(body, y=y)
        shearwater.tui.addstrs(stdscr, strs)
        time.sleep(1)


def main():
    """Main routine."""
    curses.wrapper(loop)
