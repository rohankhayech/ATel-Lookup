"""
Test suite for the web interface modules. 

Author:
    Tully Slattery

License Terms and Copyright:
    Copyright (C) 2021 Rohan Khayech

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
import json
import unittest as ut

from app import imports

test_manual = {
    "import_mode": "manual",
    "atel_num": "14726"
}

class TestWebInterface(ut.TestCase):

    def test_imports_manual(self):
        print('hello!')
        imports(test_manual)

# Run suite. 
if __name__ == '__main__':
    ut.main()