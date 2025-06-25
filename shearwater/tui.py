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
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)
