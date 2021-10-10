"""
Backend integration test for search requirements. (FR...)

Author:
    Ryan Martin

License Terms and Copyright:
    Copyright (C) 2021 Rohan Khayech, Tully Slattery, Nathan Sutardi

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
from app import app 


class TestFR6:
    ''' Functional Requirement 6:
        Description: The software must allow the user to search for ATels by
        Object ID.
    '''
    pass #NYI


class TestFR7:
    ''' Functional Requirement 7:
        Description: The software must retrieve and store object aliases and coordinates from SIMBAD when 
        an unknown object ID is entered as a search term, or 60 days have elapsed since the last update 
        for the specified object. The software must also link all reports that reference the specified 
        object.
    '''
    pass #NYI


class TestFR8:
    ''' Functional Requirement 8:
        Description: The software must allow the user to search for ATels by
        a coordinate range.
    '''
    pass #NYI


class TestFR10:
    ''' Functional Requirement 10:
        Description: The software must allow the user to search for ATels with any combination of a free-text 
        string, keyword selection and object (either object ID or coordinates) within a single query.
    '''
    pass #Partially implemented.