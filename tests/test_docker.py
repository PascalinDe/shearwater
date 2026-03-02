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
:synopsis: Docker API test cases.
"""

# standard library imports
import json
import unittest

# third party imports
# library specific imports
import shearwater.docker

from tests import DATA_DIR


class TestDockerAPI(unittest.TestCase):
    """Test Docker API."""

    def test_readfile(self):
        """Test reading file object associated with the socket.

        Trying: raw HTTP response
        Expecting: decoded HTTP response
        """
        for name in ("df.txt", "events.txt", "info.txt", "version.txt"):
            with open(DATA_DIR / "decoded" / name, mode="rb") as fp:
                expected = b"".join(fp.readlines())
            with open(DATA_DIR / "raw" / name, mode="rb") as fp:
                actual = shearwater.docker.readfile(fp)
            self.assertEqual(actual, expected)

    def test_parse_http_response(self):
        """Test parsing HTTP response.

        Trying: decoded HTTP response
        Expecting: parsed HTTP response
        """
        for name in ("df", "events", "info", "version"):
            with open(DATA_DIR / "decoded" / f"{name}.txt", mode="rb") as fp:
                response = b"".join(fp.readlines())
            actual = shearwater.docker.parse_http_response(response)
            with open(DATA_DIR / "parsed" / f"{name}.json") as fp:
                expected = json.load(fp)
            self.assertEqual(actual, expected)
