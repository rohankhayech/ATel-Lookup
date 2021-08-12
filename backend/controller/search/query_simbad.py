"""Interface for querying the SIMBAD astronomical database.

These functions are used to access the SIMBAD database, providing a way to
search by name (ID) or coordinates. Data is formatted appropriately. 

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


from typing import Union


from astropy.coordinates import SkyCoord
from astropy.table import Table
from astroquery.simbad import Simbad as simbad

from urllib3.exceptions import NewConnectionError

from requests import ConnectionError, HTTPError


# The name of the object ID column in the Astroquery Table data structure. 
IDS_COLUMN = "ID"
MAIN_IDS_COLUMN = "MAIN_ID"
RA_COLUMN = "RA"
DEC_COLUMN = "DEC"


# Mirror for the SIMBAD database.
# Using the Harvard mirror.
MIRROR = "http://simbad.cfa.harvard.edu/simbad/sim-script"


"""
Error class for a failed connection to the SIMBAD database.
"""
class QuerySimbadError(Exception):
    pass


# Helper functions (private)


def _get_coords_from_table(table: Table) -> SkyCoord:
    ''' Retrieve the coordinates of an object from an Astropy Table 
        data structure. 

    Args:
        table (astropy.table.Table): The data structure.

    Returns: 
        SkyCoord: The coordinates of the object retrieved from the table.

    Raises:
        ValueError: if the table does not provide right ascension and 
        declination columns. 
    '''
    if RA_COLUMN in table.colnames and DEC_COLUMN in table.colnames:
        # The table will always have one row in it, as if the object
        # was not found by SIMBAD, a UserWarning is raised. 
        ra = table[RA_COLUMN][0].astype('str')
        dec = table[DEC_COLUMN][0].astype('str')

        return SkyCoord(ra, dec, frame='icrs', unit=('hourangle', 'deg'))
    else:
        raise ValueError("Table does not contain the RA and DEC columns")


def _get_names_from_table(table: Table) -> list[str]:
    """ Retrieve the list of names stored in a Table data structure. 
    The table must contain the columns identifed by the IDS_COLUMN or the 
    MAIN_IDS_COLUMN constants in this file to contain the list of names. 

    Args:
        table (Table): Table data structure

    Returns:
        list[str]: List of object identifiers extracted from the table. 
    """
    # The table contains aliases (list of IDS)
    if IDS_COLUMN in table.colnames:
        column_name = IDS_COLUMN
    # The table only contains MAIN_IDS
    elif MAIN_IDS_COLUMN in table.colnames:
        column_name = MAIN_IDS_COLUMN
    # The table does not contain any names
    else:
        return []
    
    # Retrieve the names column.
    column = table[column_name].data
    lst = []

    # The type is converted to str. 
    # Astropy will either return the IDs as an array of bytes or an object. 
    for item in list(column):
        if type(item) is not str:
            lst.append(item.astype('str'))
        else:
            lst.append(item)

    return lst


def _get_aliases(id: str) -> list[str]:
    """ Queries the SIMBAD database by an object name/identifier and returns the 
        list of alternative names (aliases). 

    Args:
        id (str): The object identifier. 

    Returns:
        list[str]: A list of aliases. 
    """
    aliases_table = simbad.query_objectids(id)
    aliases_list = _get_names_from_table(aliases_table)
    return aliases_list


# Public functions. 


def query_simbad_by_coords(coords: SkyCoord, 
                           radius: float=10.0, # DEFAULT_RADIUS
) -> dict[str, list[str]]:
    """ Queries the SIMBAD database by an exact coordinate if the radius is zero, 
        or a regional area if the radius is non-zero. 

    Args:
        coords (SkyCoord): The exact coordinates or region to search for
            objects within. 
        radius (float): A value, in arcseconds, for the radius of the 
            region. By default, the radius is set to 10.0 arcsecs, however it
            can be between 0.0 (exact coordinates) and 20.0 (maximum allowed). 
    Returns:
        dict[str, list[str]]: A dictionary where the key is the MAIN_ID of an 
            object found in the coordinate range, and the value is a list of 
            aliases retrieved from SIMBAD related to the MAIN_ID. 
    Raises:
        ValueError: If the radius is invalid. 
        QuerySimbadError: if a network error occurs while contacting the 
            SIMBAD server using the Astroquery package.     
    """
    return dict("", []) # Stub


def query_simbad_by_name(object_name: str, 
                         get_aliases: bool=True
) -> tuple[str, SkyCoord, Union(list[str], None)]:
    """ Queries the SIMBAD database by an object identifier string. 

    Args:
        object_name (str): An object MAIN_ID or alias. 
        get_aliases (bool): Specify whether the aliases for the object should
            be retrieved. Defaults to True. If True, an alias list will
            be returned by this function, otherwise only the coordinates
            will be returned. 
    Returns:
        str: The object's MAIN_ID as listed in the SIMBAD database. 
        SkyCoord: The object's coordinates, retrieved from SIMBAD. 
        list[str]: A list of aliases for the object, returned only if 
            get_aliases == True.
    Raises:
        QuerySimbadError: if a network error occurs while contacting the 
            SIMBAD server using the Astroquery package. 
    """
    # Set the mirror. 
    simbad.SIMBAD_URL = MIRROR

    try:
        table = simbad.query_object(object_name)

        if table == None:
            # The object does not exist.
            return None 

        # Get the MAIN_ID and the coordinates from the table. 
        # The table may be empty (non-result), which means these 
        # functions will return 
        main_id = _get_names_from_table(table)[0]
        coords = _get_coords_from_table(table)

        if get_aliases:
            return main_id, coords, _get_aliases(object_name)

        return main_id, coords
    except ConnectionError as e:
        raise QuerySimbadError(f"Failed to establish a network connection: {str(e)}")
    except HTTPError as e:
        raise QuerySimbadError(str(e))