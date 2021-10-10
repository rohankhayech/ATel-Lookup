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
from multiprocessing import Value
from astropy.coordinates import SkyCoord
from typing import Tuple
from model.ds.search_filters import KeywordMode
from enum import Enum
import re
from model.constants import FIXED_KEYWORDS

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
    try:
        date_obj = datetime.strptime(date_string,"%Y-%m-%d")
    except ValueError as e:
        raise ValueError("Incorrect date format, ensure they are: dd/mm/yyyy")
    return date_obj


def parse_search_coords(ra: str, dec: str) -> SkyCoord:
    '''Parse coordinates into a SkyCoord object.

    Args:
        ra (str): RA coords
        dec (str): Declination coords
    
    Returns:
        SkyCoord: A SkyCoord object representing the parsed coordinates.

    Note:
        This function only takes valid data, and will raise an exception if the data is invalid. Ensure this function is called after
        valid_ra and valid_dec have been called with no errors. 

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
    ra_str = str(ra)
    h_value = 0
    m_value = 0
    s_value = 0.0
    if ra_str == "" or ra_str == None:
        raise ValueError("No right ascension coordinates given")

    if ("h" in ra_str and "m" in ra_str and "s" in ra_str): # for the hms format of coords
        string_split = re.split('h|m|s',ra_str)
    elif (":" in ra_str): # for the xx:xx:xx format of coords
        string_split = ra_str.split(':')
    else:
        bool_response = False
        raise ValueError("Incorrect format for right ascension coordinates, ensure they are: hh:mm:ss.ssss")
        
    # making the split variables the correct data types
    if bool_response == True and len(string_split) == 3 and (string_split[0] != "" or string_split[1] != "" or string_split[2] != ""): 
        h_value = int(string_split[0]) 
        m_value = int(string_split[1])
        s_value = float(string_split[2])
    else:
        raise ValueError("Incorrect format for right ascension coordinates, ensure they are: hh:mm:ss.ssss")

    if h_value == None:
        bool_response = False
        raise ValueError("No hour value given for right ascension coordinate")
    if m_value == None:
        bool_response = False
        raise ValueError("No minute value given for right ascension coordinate")
    if s_value == None:
        bool_response = False
        raise ValueError("No second value given for right ascension coordinate")

    # checking validity of values with their min max ranges
    if bool_response == True:
        if h_value < -24 or h_value > 24:
            bool_response = False
            raise ValueError("Right ascension hour value is outside of range (-24 to 24)")
        elif m_value < 0 or m_value >= 60:
            bool_response = False
            raise ValueError("Right ascension minute value is outside of range (0 to 60)")
        elif s_value < 0.0 or s_value >= 60.0:
            bool_response = False
            raise ValueError("Right ascension second value is outside of range (0 to 60)")

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
    if dec == "" or dec == None:
        raise ValueError("No declination coordinates given")

    if ("d" in dec and "m" in dec and "s" in dec): # for the hms format of coords
        string_split = re.split('d|m|s',dec)
    elif (":" in dec): # for the xx:xx:xx format of coords
        string_split = dec.split(':')
    else:
        bool_response = False
        raise ValueError("Incorrect format for declination coordinates, ensure they are: dd:mm:ss.ssss")

    # making the split variables the correct data types
    if bool_response == True and len(string_split) == 3 and (string_split[0] != "" or string_split[1] != "" or string_split[2] != ""):
        d_value = int(string_split[0])
        m_value = int(string_split[1])
        s_value = float(string_split[2])
    else:
        raise ValueError("Incorrect format for right ascension coordinates, ensure they are: hh:mm:ss.ssss")

    if d_value == None:
        bool_response = False
        raise ValueError("No degree value given for declination coordinate")
    if m_value == None:
        bool_response = False
        raise ValueError("No minute value given for declination coordinate")
    if s_value == None:
        bool_response = False
        raise ValueError("No second value given for declination coordinate")

    # checking validity of values with their min max ranges
    if bool_response == True:
        if d_value < -90 or d_value > 90:
            bool_response = False
            raise ValueError("Declination degree value is outside of range (-90 to 90)")
        elif m_value < 0 or m_value >= 60:
            bool_response = False
            raise ValueError("Declination minute value is outside of range (0 to 60)")
        elif s_value < 0.0 or s_value >= 60.0:
            bool_response = False
            raise ValueError("Declination second value is outside of range (0 to 60)")

    return bool_response 


def valid_radius(rad: str) -> bool:
    '''Validates the given radius value to ensure it is a ‘possible’ radius value

    Args:
        rad (float): A float value for the radius
    
    Returns:
        bool: A boolean representing if the value is in the correct range

    '''
    bool_response = True
    if rad == "" or rad == None:
        rad = 10.0
        
    rad_float = float(rad)

    # checking validity of the radius with its min max ranges
    if rad_float > 20.0 or rad_float < 0.0:
        bool_response = False
        raise ValueError("Radius value is out of range (0 to 20)")

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


def search_mode_check(search_mode_in: str) -> bool:
    '''
    '''
    bool_response = True

    if search_mode_in != "coords" and search_mode_in != "name":
        raise ValueError("Search mode not coords or name")

    return bool_response

def req_fields_check(search_data_in: str, keywords_in: str, keyword_mode_in: str, term_in: str) -> bool:
    '''
    '''
    bool_response = True

    if (search_data_in == None and keywords_in == None and keyword_mode_in == None and term_in == None):
        raise ValueError("Required fields not given, provide a free text search, keyword, object name or coordinates.")

    return bool_response

def valid_date_check(start_date_obj: datetime, end_date_obj: datetime) -> bool:
    '''
    '''
    bool_response = True

    if start_date_obj == None:
        start_date_obj = parse_date_input("1900-01-01")

    if end_date_obj == None:
        end_date_obj = datetime.now()

    if start_date_obj > end_date_obj:
        raise ValueError("The start date is greater than the end date.")
    if end_date_obj < start_date_obj:
        raise ValueError("The end date is less than the start date.")
    if start_date_obj > datetime.now():
        raise ValueError("The start date is a date in the future.")
    if end_date_obj > datetime.now():
        raise ValueError("The end date is a date in the future.")

    return bool_response

def keywords_check(keywords_in: str) -> bool:
    '''
    '''
    bool_response = True
    
    for x in keywords_in:
        if x not in FIXED_KEYWORDS:
            raise ValueError("Keywords given were not part of FIXED_KEYWORDS list")

    return bool_response


def keyword_mode_check(keyword_mode_in: str) -> bool:
    '''
    '''
    bool_response = True

    if keyword_mode_in != "all" and keyword_mode_in != "any" and keyword_mode_in != "none":
        raise ValueError("Keyword mode is not all, any or none")

    return bool_response


def valid_coords_basic_check(search_data_in: str) -> bool:
    '''
    '''
    bool_response = True
    print("\n")
    print(search_data_in)
    print("\n")
    if search_data_in == None or search_data_in == "":
        raise ValueError("Right ascension and declination coordinates must be provided")

    if search_data_in[0] == "" or search_data_in[1] == "":
        raise ValueError("Right ascension and declination coordinates must be provided")
             

    return bool_response


def none_check(term_in: str, search_mode_in: str, search_data_in: str, keywords_in: str, keyword_mode_in: str, start_date_in: str, end_date_in: str) -> bool:
    '''
    '''
    bool_response = True

    if (term_in == None or search_mode_in == None or search_data_in == None
            or keywords_in == None or keyword_mode_in == None
            or start_date_in == None or end_date_in == None):
        raise ValueError("Bad JSON request, not all fields recieved")

    return bool_response