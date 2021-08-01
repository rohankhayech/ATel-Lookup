from typing import List
from datetime import datetime
from astropy.coordinates import SkyCoord
from astropy.table import Table


def search_reports_by_coords(search_filters: SearchFilters, 
                             coords: SkyCoord, 
                             radius: float=10.0
) -> List[ReportResult]:
    ''' Performs an immediate query of the SIMBAD database by the coordinate
        range and retrieves matching reports from the local database. 

    Args: 
        search_filters (SearchFilters): Filters for the frontend search. 
        coords (SkyCoord): The coordinates that define the region search criteria. 
        radius (float): The radius, in arcseconds, that defines the size of the
            region. 10.0 arcsecs by default. Should be validated beforehand. 

    Returns:
        List[ReportResult]: The reports found in the local database that match
            the coordinate/region criteria. 

    Raises:
        QuerySimbadError: When the SIMBAD server is unavailable. The error is
            raised as a connection to the server is required to perform a coordinate
            search. 
    '''
    return [] # Stub


def search_reports_by_id(search_filters: SearchFilters, name: str) -> List[ReportResult]:
    ''' Query the local database and the SIMBAD database by an object identifier
        and return the reports that match. 

    Args:
        search_filters (SearchFilters): Filters for the frontend search. 
        name (str): The object identifier. 

    Returns:
        List[ReportResult]: The reports found in the local database that match
            the name. 
    '''
    return [] # Stub


def check_object_updates(alias: str, last_update: datetime):
    ''' Check if an object, specified by its identifier, requires an update. 
        (i.e., more than 60 days have elapsed since its last update). If so, 
        update the object. 
    
    Args: 
        alias (str): The object's identifier (can be an alias or MAIN_ID). 
        last_update (datetime): The date and time the object was last updated. 
    '''
    pass # Stub


def _get_coords_from_table(table: Table) -> SkyCoord:
    ''' Retrieve the coordinates of an object from an Astropy Table 
        data structure. 

    Args:
        table (astropy.table.Table): The data structure.

    Returns: 
        SkyCoord: The coordinates of the object retrieved from the table.
    '''
    return SkyCoord(0.0, 0.0) # Stub