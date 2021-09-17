""" This file contains all of the relevant private web interface functions.

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
from astropy.coordinates import SkyCoord
import json
from typing import Tuple
from model.ds.search_filters import KeywordMode
from enum import Enum
import enum


def parse_date_input(date_string: str) -> datetime:
    '''This function transforms an imported date string into a Python datetime object 
    that will be used for the rest of the system.

    Args:
        date_string (str): A string representing a date
    
    Returns:
        datetime: A Python datetime object based on the parsed string. 

    '''

    date_obj = datetime.strptime(date_string,"%Y-%m-%d")

    return date_obj


def parse_search_coords(ra: float, dec: float) -> SkyCoord:
    '''Parse coordinates into a SkyCoord object.

    Args:
        ra (str): RA coords
        dec (str): Declination coords
        radius (str): Radius value
    
    Returns:
        SkyCoord: A SkyCoord object representing the parsed coordinates. 

    '''
    sky_coord_out = None

    if valid_ra(ra) == True and valid_dec(dec) == True:
        sky_coord_out = SkyCoord(ra, dec, frame="icrs", unit=("deg", "deg"))

    return sky_coord_out 


def valid_ra(ra: str) -> bool:
    '''Validates the given right-ascension coordinates to ensure they are 
    ‘possible’ RA coordinates

    Args:
        ra (str): A string representing a right-ascension
    
    Returns:
        bool: A boolean representing if the string is a valid coordinate

    '''
    bool_response = True
    ra_float = float(ra)
    if ra_float > 360 or ra_float < 0:
        bool_response = False

    return bool_response 


def valid_dec(dec: str) -> bool:
    '''Validates the given declination coordinates to ensure they are 
    ‘possible’ declination coordinates

    Args:
        dec (str): A string representing declination coords
    
    Returns:
        bool: A boolean representing if the string is a valid coordinate

    '''
    bool_response = True
    dec_float = float(dec)

    if dec_float > 90.0 or dec_float < -90.0:
        bool_response = False

    return bool_response 


def valid_radius(rad: str) -> bool:
    '''Validates the given radius value to ensure it is a ‘possible’ radius value

    Args:
        rad (float): A float value for the radius
    
    Returns:
        bool: A boolean representing if the value is in the correct range

    '''
    bool_response = True
    rad_float = float(rad)

    if rad_float > 20.0 or rad_float < 0.0:
        bool_response = False

    return bool_response 


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