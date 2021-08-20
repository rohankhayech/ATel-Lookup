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
from model.constants import DEFAULT_RADIUS
from model.ds.report_types import ReportResult
from model.ds.search_filters import SearchFilters
import model.db_helper as db
from controller.search import query_simbad as qs


def search_reports_by_coords(search_filters: SearchFilters, 
                             coords: SkyCoord, 
                             radius: float=DEFAULT_RADIUS
) -> list[ReportResult]:
    """ Performs an immediate query of the SIMBAD database by the coordinate
        range and retrieves matching reports from the local database. 

    Args: 
        search_filters (SearchFilters): Filters for the frontend search. 
        coords (SkyCoord): The coordinates that define the region search criteria. 
        radius (float): The radius, in arcseconds, that defines the size of the
            region. 10.0 arcsecs by default. Should be validated beforehand. 

    Returns:
        list[ReportResult]: The reports found in the local database that match
            the coordinate/region criteria. 

    Raises:
        QuerySimbadError: When the SIMBAD server is unavailable. The error is
            raised as a connection to the server is required to perform a coordinate
            search. 
    """
    return [] # Stub


def search_reports_by_name(search_filters: SearchFilters, name: str) -> list[ReportResult]:
    """ Query the local database and the SIMBAD database by an object identifier
        and return the reports that match. 

    Args:
        search_filters (SearchFilters): Filters for the front-end search. 
        name (str): The object identifier. 

    Returns:
        list[ReportResult]: The reports found in the local database that match
            the name, or None if no object is found. 
    """
    # Get a list of existing reports in the database. 
    existing_reports = False # Stub, TODO: awaiting db.object_exists() function. 
    report_exists = existing_reports is not None

    if report_exists:
        # Check each object for updates. 
        for object in existing_reports:
            check_object_updates(object)
    else:
        query_result = qs.query_simbad_by_name(name)
        if query_result is not None:
            main_id = query_result[0]
            coordinates = query_result[1]
            aliases = query_result[2]
            db.add_object(main_id, coordinates, aliases)
        else:
            # There were no reports found in the local database
            # and no results found by SIMBAD, therefore there is no result.
            return None
    
    reports = db.find_reports_by_object(search_filters, name)
    coords = db.get_object_coords(reports[0])

    for additional_report in db.find_reports_in_coord_range(search_filters, coords, 0.0):
        reports.append(additional_report)

    return reports


def check_object_updates(object: ReportResult):
    """ Check if an object, specified by its identifier, requires an update. 
        (i.e., more than 60 days have elapsed since its last update). If so, 
        update the object. 
    
    Args: 
        object (ReportResult): The object in the database. 
    """
    pass # Stub