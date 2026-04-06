#    This file is part of Shearwater.
#    Copyright (C) 2026  Carine Dengler
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
import curses.textpad

# third party imports
# library specific imports


NLINES_VERSION = 4


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
    curses.cbreak()
    curses.noecho()
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
    curses.init_pair(9, 0, curses.COLOR_BLUE)


def textbox(prompt, parent_win, nlines, ncols, validator):
    """Handle textbox.

    :param str prompt: prompt
    :param window parent_win: parent window
    :param int nlines: height (prompt excluded)
    :param int ncols: width (prompt excluded)
    :param function validator: validator

    :returns: input
    """
    prompt = f"{prompt}: (hit Ctrl-G to send)"
    y, x = parent_win.getparyx()
    max_y, max_x = parent_win.getmaxyx()
    uly = 0
    ulx = max_x // 2 - (ncols + len(prompt)) // 2
    lry = uly + nlines + 1 + 1
    if lry > max_y:
        raise ValueError(f"textbox height exceeds maximum height ({lry} > {max_y})")
    lrx = ulx + ncols + len(prompt) + 1 + 1
    if lrx > max_x:
        raise ValueError(f"textbox width exceeds maximum width ({lrx} > {max_x})")
    curses.textpad.rectangle(
        parent_win,
        uly,
        ulx,
        lry,
        lrx,
    )
    uly += 1
    ulx += 1
    parent_win.addstr(uly, ulx, prompt)
    parent_win.refresh()
    uly += 1
    subwin = parent_win.subwin(
        nlines,
        ncols + len(prompt),
        y + uly,
        x + ulx,
    )
    textbox = curses.textpad.Textbox(subwin)
    textbox.edit()
    input_ = textbox.gather()
    parent_win.erase()
    return validator(input_)


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
        self.scr["std"].nodelay(True)
