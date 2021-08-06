"""The main search interface. 

The public function in this file perform the search processes for each
type of search (name or coordinate search). Both functions have a different
process for searching, including when and how they access the SIMBAD database. 
For accessing/searching using the SIMBAD database directly, see query_simbad.py. 

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


from datetime import datetime
from astropy.coordinates import SkyCoord


def search_reports_by_coords(search_filters: SearchFilters, 
                             coords: SkyCoord, 
                             radius: float=10.0
) -> list[ReportResult]:
    """ Performs an immediate query of the SIMBAD database by the coordinate
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
    """
    return [] # Stub


def search_reports_by_id(search_filters: SearchFilters, name: str) -> list[ReportResult]:
    """ Query the local database and the SIMBAD database by an object identifier
        and return the reports that match. 

    Args:
        search_filters (SearchFilters): Filters for the frontend search. 
        name (str): The object identifier. 

    Returns:
        List[ReportResult]: The reports found in the local database that match
            the name. 
    """
    return [] # Stub


def check_object_updates(alias: str, last_update: datetime):
    """ Check if an object, specified by its identifier, requires an update. 
        (i.e., more than 60 days have elapsed since its last update). If so, 
        update the object. 
    
    Args: 
        alias (str): The object's identifier (can be an alias or MAIN_ID). 
        last_update (datetime): The date and time the object was last updated. 
    """
    pass # Stub