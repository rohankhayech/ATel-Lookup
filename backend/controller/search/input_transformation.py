""" The input transformation module is responsible for transforming inputs into more readable/usable
    formats

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


def parse_date_input(date_string: str) -> datetime:
    '''This function transforms an imported date string into a Python datetime object 
    that will be used for the rest of the system.

    Args:
        date_string (str): A string representing a date
    
    Returns:
        datetime: A Python datetime object based on the parsed string. 

    '''
    return 1/1/2000 #stub


def parse_search_coords(ra: str, dec: str, radius: str) -> SkyCoord:
    '''Parse coordinates into a SkyCoord object.

    Args:
        ra (str): RA coords
        dec (str): Declination coords
        radius (str): Radius value
    
    Returns:
        SkyCoord: A SkyCoord object representing the parsed coordinates. 

    '''
    return SkyCoord(0,0,0) #stub