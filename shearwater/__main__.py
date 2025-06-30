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
import curses

# third party imports
# library specific imports
import shearwater.tui
import shearwater.docker


def loop_through(stdscr):
    """Loop through user interaction.

    :param window stdscr: initial window
    """
    shearwater.tui.init()
    while True:
        response = shearwater.docker.parse_http_response(
            shearwater.docker.send(shearwater.docker.VERSION),
        )
        status_code = response["start_line"].split(" ")[1]
        if status_code == "200":
            shearwater.tui.display_version(stdscr, response["body"])
        else:
            shearwater.tui.display_error(stdscr, status_code, response["body"])


def main():
    """Main routine."""
    curses.wrapper(loop_through)
