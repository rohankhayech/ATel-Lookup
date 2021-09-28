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
from typing import Tuple
from model.ds.search_filters import KeywordMode
from enum import Enum
import re

class InvalidKeywordError(Exception):
    pass


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


def parse_search_coords(ra: str, dec: str) -> SkyCoord:
    '''Parse coordinates into a SkyCoord object.

    Args:
        ra (str): RA coords
        dec (str): Declination coords
    
    Returns:
        SkyCoord: A SkyCoord object representing the parsed coordinates. 

    '''
    sky_coord_out = None

    sky_coord_out = SkyCoord(ra, dec, frame="icrs", unit=("hourangle", "deg"))

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
    h_value = 0
    m_value = 0
    s_value = 0

    if ("h" in ra and "m" in ra and "s" in ra): # for the hms format of coords
        string_split = re.split('h|m|s',ra)
    elif (":" in ra): # for the xx:xx:xx format of coords
        string_split = ra.split(':')
    else:
        bool_response = False
    
    # making the split variables the correct data types
    if bool_response == True: 
        h_value = int(string_split[0]) 
        m_value = int(string_split[1])
        s_value = float(string_split[2])

    if h_value == 0 or h_value == None:
        bool_response = False
    if m_value == 0 or m_value == None:
        bool_response = False
    if s_value == 0 or s_value == None:
        bool_response = False

    # checking validity of values with their min max ranges
    if bool_response == True:
        if h_value < -24 and h_value > 24:
            bool_response = False
        elif m_value < 0 and m_value > 60:
            bool_response = False
        elif s_value < 0.0 and s_value > 60.0:
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
    d_value = 0
    m_value = 0
    s_value = 0

    if ("d" in dec and "m" in dec and "s" in dec): # for the hms format of coords
        string_split = re.split('d|m|s',dec)
    elif (":" in dec): # for the xx:xx:xx format of coords
        string_split = dec.split(':')
    else:
        bool_response = False

    # making the split variables the correct data types
    if bool_response == True:
        d_value = int(string_split[0])
        m_value = int(string_split[1])
        s_value = float(string_split[2])

    if d_value == 0 or d_value == None:
        bool_response = False
    if m_value == 0 or m_value == None:
        bool_response = False
    if s_value == 0 or s_value == None:
        bool_response = False

    # checking validity of values with their min max ranges
    if bool_response == True:
        if d_value < 0 and d_value > 360:
            bool_response = False
        elif m_value < 0 and m_value > 60:
            bool_response = False
        elif s_value < 0.0 and s_value > 60.0:
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

    # checking validity of the radius with its min max ranges
    if rad_float > 20.0 or rad_float < 0.0:
        bool_response = False

    return bool_response 


def parse_keyword_mode(keyword_mode: str) -> KeywordMode: 
    '''To check that the user has selected either “none”, “any” or “all” as a 
    keyword mode for the search. These options are in the form of an enumeration. 

    Args:
        keyword_mode (str): an string representing 
    
    Returns:
        KeywordMode: enum representing a keywordmode

    '''
    # creating enum version of keyword_mode_in
    if keyword_mode == "all":
        keyword_mode_enum_out = KeywordMode.ALL
    elif keyword_mode == "any":
        keyword_mode_enum_out = KeywordMode.ANY
    elif keyword_mode == "none":
        keyword_mode_enum_out = KeywordMode.NONE
    else:
        raise InvalidKeywordError()

    return keyword_mode_enum_out 


def valid_atel_num(atel_num: int) -> bool:
    '''Checks whether the supplied number is a possible ATel number. 

    Args:
        atel_num (int): A integer representing an ATel number.
    
    Returns:
        bool: A boolean representing if the ATel number is valid.

    '''
    bool_response = True

    if atel_num == None:
        bool_response = False

    if bool_response == True and atel_num <= 0:
        bool_response = False

    return bool_response 