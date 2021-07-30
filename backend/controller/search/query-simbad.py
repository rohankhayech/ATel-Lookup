from typing import Dict, Tuple, List
from astropy.coordinates import SkyCoord


def query_simbad_by_coords(coords: SkyCoord, radius: float=10.0) -> Dict[str, List[str]]:
    ''' Queries the SIMBAD database by an exact coordinate if the radius is zero, 
        or a regional area if the radius is non-zero. 

    Args:
        coords (SkyCoord): The exact coordinates or region to search for
            objects within. 
        radius (float): A value, in arcseconds, for the radius of the 
            region. By default, the radius is set to 10.0 arcsecs, however it
            can be between 0.0 (exact coordinates) and 20.0 (maximum allowed). 
    Returns:
        Dict[str, List[str]]: A dictionary where the key is the MAIN_ID of an 
            object found in the coordinate range, and the value is a list of 
            aliases retrieved from SIMBAD related to the MAIN_ID. 
    Raises:
        ValueError: If the radius is invalid. 
        QuerySimbadError: if a network error occurs while contacting the 
            SIMBAD server using the Astroquery package.     
    '''
    return dict("", [])


def _query_simbad_by_name(object_name: str, 
                          get_aliases: bool=True
) -> Tuple[str, SkyCoord, List[str]]:
    ''' Queries the SIMBAD database by an object identifier string. 

    Args:
        object_name (str): An object MAIN_ID or alias. 
        get_aliases (bool): Specify whether the aliases for the object should
            be retrieved. Defaults to True. If True, an alias list will
            be returned by this function, otherwise only the coordinates
            will be returned. 
    Returns:
        str: The object's MAIN_ID as listed in the SIMBAD database. 
        SkyCoord: The object's coordinates, retrieved from SIMBAD. 
        List[str]: A list of aliases for the object, returned only if 
            get_aliases == True.
    Raises:
        QuerySimbadError: if a network error occurs while contacting the 
            SIMBAD server using the Astroquery package. 
    '''
    return "default", SkyCoord(0.0, 0.0), []