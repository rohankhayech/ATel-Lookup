""" Unit testing suite for the search module (internal)

These functions include mocking for other modules (i.e., the database 
module) to ensure the search components are tested in isolation. 

Author:
    Ryan Martin

License Terms and Copyright:
    Copyright (C) 2021 Ryan Martin

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


import unittest as ut 
from controller.search import search

# Mocking functions. 

def none_return():
    return None 


def db_function_stub():
    pass 


class TestObjectUpdates(ut.TestCase):
    def setUp(self):
        pass 