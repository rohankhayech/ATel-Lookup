"""
Contains helper methods used for type checking.

Author:
    Rohan Khayech

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

import unittest

def list_is_type(lst:list,typ:type)->bool:
    """
    Checks if a given list is of a single type.

    Args:
        lst (list): The list to check.
        typ (type): The type to check.

    Returns:
        bool: True if all elements in the list are of the specified type.
    """
    if type(lst) == list and type(typ) == type:
        if lst:
            return all(isinstance(e, typ) for e in lst)
        else:
            return False
    else:
        return False



#Test suite
class _Test(unittest.TestCase):
    def testEmpty(self):
        self.assertFalse(list_is_type([],int))
    
    def testAllInt(self):
        self.assertTrue(list_is_type([1,2],int))
        self.assertFalse(list_is_type([1,2], str))

    def testAllStr(self):
        self.assertFalse(list_is_type(["a",'b'],int))
        self.assertTrue(list_is_type(["a",'b'],str))

    def testMixed(self):
        self.assertFalse(list_is_type([1, "b"], int))
        self.assertFalse(list_is_type([1, "b"], str))

    def testNotAList(self):
        self.assertFalse(list_is_type(5, int))

    def testNotAType(self):
        self.assertFalse(list_is_type([1,2], 5))


if __name__ == '__main__':
    unittest.main()
