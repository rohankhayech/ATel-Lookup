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


from astropy.coordinates import SkyCoord
from astropy.table import Table


"""
Error class for a failed connection to the SIMBAD database.
"""
class QuerySimbadError(Exception):
    pass


def _get_coords_from_table(table: Table) -> SkyCoord:
    ''' Retrieve the coordinates of an object from an Astropy Table 
        data structure. 

    Args:
        table (astropy.table.Table): The data structure.

    Returns: 
        SkyCoord: The coordinates of the object retrieved from the table.
    '''
    return SkyCoord(0.0, 0.0) # Stub


def _table_to_list(table: Table) -> list[str]:
    """ Convert an Astroquery Table data structure to a Python list. 

    Args:
        table (Table): Table data structure

    Returns:
        list[str]: List of object identifiers extracted from the table. 
    """
    return []


def query_simbad_by_coords(coords: SkyCoord, radius: float=10.0) -> dict[str, list[str]]:
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


def _query_simbad_by_name(object_name: str, 
                          get_aliases: bool=True
) -> tuple[str, SkyCoord, list[str]]:
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
    return "default", SkyCoord(0.0, 0.0), [] # Stub