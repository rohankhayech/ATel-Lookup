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


from astropy.coordinates import SkyCoord

from datetime import datetime

from model.constants import DEFAULT_RADIUS
from model.ds.report_types import ReportResult
from model.ds.search_filters import SearchFilters, DateFilter
import model.db.db_interface as db
from controller.search import query_simbad as qs


###########################
# Search module constants #
###########################


# The amount of days elapsed before updating an object. 
UPDATE_OBJECT_DAYS: int = 60 


####################
# Public functions #
####################


def search_reports_by_coords(search_filters: SearchFilters,
                             date_filter: DateFilter,
                             coords: SkyCoord, 
                             radius: float=DEFAULT_RADIUS
) -> list[ReportResult]:
    """ Performs an immediate query of the SIMBAD database by the coordinate
        range and retrieves matching reports from the local database. 

    Args: 
        search_filters (SearchFilters): Filters for the frontend search. 
        date_filter (DateFilter): Date filter for the frontend search.
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


def search_reports_by_name(
    search_filters: SearchFilters = None,
    date_filter: DateFilter = None,
    name: str = None
) -> list[ReportResult]:
    """ Query the local database and the SIMBAD database by an object identifier
        and return the reports that match. 

    Args:
        search_filters (SearchFilters): Filters for the front-end search. 
        date_filter (DateFilter, optional): Date filter for the front-end search. 
        name (str): The object identifier. 

    Returns:
        list[ReportResult]: The reports found in the local database that match
            the name.

    Raises:
        QuerySimbadError: If there is an issue connecting to the SIMBAD server. 
            It's important this error is handled by the front-end as an error/warning
            message should be displayed to the user. 
        ValueError: If SearchFilters and name is None. 
    """
    if search_filters is None and name is None:
        raise ValueError("SearchFilters and name cannot both be None.")

    coordinates = None
    by_coord_range = None

    if name is not None:
        # Check if the object already exists in the local database. 
        exists, last_updated = db.object_exists(name)

        # Check if the object exists in the database. 
        if exists:
            # The object exists in the local database, check to see if it needs to be updated. 
            check_object_updates(name, last_updated)
            coordinates = db.get_object_coords(name)
        else:
            # The object does not exist, invoke an external (SIMBAD) search. 
            query_result = qs.query_simbad_by_name(name, True)

            if query_result is not None:
                # There is a result from the SIMBAD search. 
                # Add the object to the local database.
                main_id = query_result[0]
                coordinates = query_result[1]
                aliases = query_result[2]
                db.add_object(main_id, coordinates, aliases)

    # After update checking and external search, query the local database 
    # for all reports. 

    # Get the base reports from the database. 
    reports = db.find_reports_by_object(search_filters, date_filter, name)

    if reports is None: 
        reports = []

    if coordinates is not None:
        by_coord_range = db.find_reports_in_coord_range(search_filters, date_filter, coordinates, DEFAULT_RADIUS)
        if by_coord_range is not None:
            # Append the list with reports with the same coordinates. 
            for additional_report in by_coord_range:
                if not additional_report in reports:
                    reports.append(additional_report)

    return reports


def check_object_updates(name: str, last_updated: datetime):
    """ Check if an object, specified by its identifier, requires an update. 
        (i.e., more than 60 days have elapsed since its last update). If so, 
        update the object. 
    
    Args: 
        name (str): The object's identifier. 
        last_updated (datetime): The last updated date. 

    Raises:
        QuerySimbadError (from query_simbad.get_aliases()). 
        ObjectNotFoundError (from db_interface.add_aliases())
    """
    diff = datetime.today() - last_updated
    if diff.days >= UPDATE_OBJECT_DAYS:
        # The object requires updating, check for its aliases. 
        aliases = qs.get_aliases(name)
        db.add_aliases(name, aliases)
