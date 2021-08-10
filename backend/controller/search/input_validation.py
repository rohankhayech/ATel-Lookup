""" The input validations module is responsible for validation input on RA, Declination,
    Radius, Keyword Mode and ATeL number

Author:
    Tully Slattery

License Terms and Copyright:
    Copyright (C) 2021 Tully Slattery

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




from datetime import datetime
import json
from typing import Tuple
from backend.model.search_filters import KeywordMode
from enum import Enum
import enum


def valid_ra(ra: str) -> bool:
    '''Validates the given right-ascension coordinates to ensure they are 
    ‘possible’ RA coordinates

    Args:
        ra (str): A string representing a right-ascension
    
    Returns:
        bool: A boolean representing if the string is a valid coordinate

    '''
    return True #stub


def valid_dec(dec: str) -> bool:
    '''Validates the given declination coordinates to ensure they are 
    ‘possible’ declination coordinates

    Args:
        dec (str): A string representing declination coords
    
    Returns:
        bool: A boolean representing if the string is a valid coordinate

    '''
    return True #stub


def valid_radius(rad: float) -> bool:
    '''Validates the given radius value to ensure it is a ‘possible’ radius value

    Args:
        rad (float): A float value for the radius
    
    Returns:
        bool: A boolean representing if the value is in the correct range

    '''
    return True #stub


def valid_keyword_mode(keyword_mode: KeywordMode) -> bool:
    '''To check that the user has selected either “none”, “any” or “all” as a 
    keyword mode for the search. These options are in the form of an enumeration. 

    Args:
        keyword_mode (enum): an enum of type KeywordMode
    
    Returns:
        bool: A Boolean representing if a valid keyword mode has been chosen

    '''
    return True #stub


def valid_atel_num(atel_num: int) -> bool:
    '''Checks whether the supplied number is a possible ATel number. 

    Args:
        atel_num (int): A integer representing an ATel number.
    
    Returns:
        bool: A boolean representing if the ATel number is valid.

    '''
    return True #stub


def load_metadata() -> Tuple[datetime, int]:
    '''To get the data associated with imports, such as the last time 
    it was updated and how many reports we have.
    
    Returns:
        datetime: A Python datetime object specifying the last updated date for the database.

        int: integer – Count of reports in the database (this number is also the last ATel 
            number we have stored, as ATel reports are numbered increasingly)

    '''
    return 1/1/2000, 0 #stub


def enter_credentials(credentials: json) -> json:
    '''Validate user input and call login() function.
    
    Args:
        credentials (json): A JSON object representing a username and password.

    Returns:
        json: JSON authentication token.

    '''
    return 1/1/2000, 0 #stub
