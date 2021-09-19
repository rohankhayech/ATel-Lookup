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
from astropy.coordinates.angles import Angle
from astropy.table import Table
from astroquery.simbad import Simbad

from requests.exceptions import ConnectionError, HTTPError


#############################
# External module constants #
#############################

DEFAULT_RADIUS, RADIUS_UNIT = 10.0, 'deg'

# Mirror for the SIMBAD database.
# Using the Harvard mirror.
SIMBAD_MIRROR = "http://simbad.cfa.harvard.edu/simbad/sim-script"


# The name of the object ID column in the Astroquery Table data structure. 
IDS_COLUMN = "ID"
MAIN_IDS_COLUMN = "MAIN_ID"
RA_COLUMN = "RA"
DEC_COLUMN = "DEC"


"""
Error class for a failed connection to the SIMBAD database.
"""
class QuerySimbadError(Exception):
    pass


##############################
# Helper functions (private) #
##############################


def _get_coords_from_table(table: Table) -> SkyCoord:
    ''' Retrieve the coordinates of an object from an Astropy Table 
        data structure. 

    Args:
        table (astropy.table.Table): The data structure.

    Returns: 
        SkyCoord: The coordinates of the object retrieved from the table.

    Raises:
        ValueError: if the table does not provide right ascension and 
        declination columns, or is uninitialised.
    '''
    if table is None:
        raise ValueError("Table is uninitialised.")
    elif RA_COLUMN in table.colnames and DEC_COLUMN in table.colnames:
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
            If no names could be extracted, an empty list is returned. 

    Raises:
        ValueError: if the table is not initialised.
    """
    if table is None:
        raise ValueError("Table is not initialised")
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


def _set_mirror(): 
    """ Sets the mirror for SIMBAD to the one defined by the
        SIMBAD_MIRROR constant.
    """
    Simbad.SIMBAD_URL = SIMBAD_MIRROR


#####################
# Public functions. #
#####################


def get_aliases(id: str) -> list[str]:
    """ Queries the SIMBAD database by an object name/identifier and returns the 
        list of alternative names (aliases). 

    Args:
        id (str): The object identifier. 

    Returns:
        list[str]: A list of aliases. List is empty if no aliases exist. 

    Raises:
        QuerySimbadError: if a network error occurs while contacting the 
            SIMBAD server using the Astroquery package.  
    """
    try:
        aliases_table = Simbad.query_objectids(id)
        aliases_list = _get_names_from_table(aliases_table)
    except ConnectionError as e:
        raise QuerySimbadError(f"Failed to establish a network connection: {str(e)}")
    except HTTPError as e:
        raise QuerySimbadError(str(e))
    except UserWarning as e:
        # No aliases found.
        return [] 

    return aliases_list


def query_simbad_by_coords(coords: SkyCoord, 
                           radius: float=DEFAULT_RADIUS
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
    # Radius should be validated prior to calling this function. 
    if  radius < 0.0 or radius > 20.0:
        raise ValueError(f"Invalid radius: \"${radius}\" not in range 0.0 to 20.0.")
    if coords is None:
        raise ValueError("SkyCoord value is unknown.")
    
    # Construct the radius angle for the region search. 
    radius_angle = Angle(radius, unit=RADIUS_UNIT)

    _set_mirror()

    try:        
        table = Simbad.query_region(coords, radius_angle)

        if table is None:
            return dict()

        # For a region search, there may be multiple IDs. 
        # Get all the MAIN_IDs from the table. 
        main_ids = _get_names_from_table(table)

        # Create empty dictionary.
        results = dict()

        # Get the aliases for each ID. Assign the alias list to 
        # the value of the main ID.
        for id in main_ids:
            results[id] = get_aliases(id)

        return results
    except ConnectionError as e:
        raise QuerySimbadError(f"Failed to establish a network connection: {str(e)}")
    except HTTPError as e:
        raise QuerySimbadError(str(e))
    except UserWarning as e:
        # No object found.
        return dict()


def query_simbad_by_name(object_name: str, 
                         retrieve_aliases: bool=True
) -> tuple[str, SkyCoord, list[str]]:
    """ Queries the SIMBAD database by an object identifier string. 

    Args:
        object_name (str): An object MAIN_ID or alias. 
        retrieve_aliases (bool): Specify whether the aliases for the object should
            be retrieved. Defaults to True. If True, an alias list will
            be returned by this function, otherwise only the coordinates
            will be returned. 
    Returns:
        str: The object's MAIN_ID as listed in the SIMBAD database. 
        SkyCoord: The object's coordinates, retrieved from SIMBAD. 
        list[str]: A list of aliases for the object, returned only if 
            retrieve_aliases == True.
    Raises:
        QuerySimbadError: if a network error occurs while contacting the 
            SIMBAD server using the Astroquery package. 
    """
    _set_mirror()

    try:
        table = Simbad.query_object(object_name)

        if table is None:
            # The object does not exist.
            return None

        # Get the MAIN_ID and the coordinates from the table. 
        # The table may be empty (non-result), which means these 
        # functions will return 
        main_id = _get_names_from_table(table)[0]
        coords = _get_coords_from_table(table)

        if retrieve_aliases:
            return main_id, coords, get_aliases(object_name)

        return main_id, coords, []
    except ConnectionError as e:
        raise QuerySimbadError(f"Failed to establish a network connection: {str(e)}")
    except HTTPError as e:
        raise QuerySimbadError(str(e))
    except UserWarning as e:
        # No object found.
        return None