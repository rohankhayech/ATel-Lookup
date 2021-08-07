"""
The database interface handles all interactions with the local database including adding, modifying and querying data. This component is responsible for all database operations and provides the complete set of methods needed to access the application’s stored data.

Other components do not have to describe raw SQL queries and data/criteria should be imported in the format that makes sense for the application. The database component handles translating this data into the format defined in the data schema or required by SQL queries.
The database should not be accessed directly outside of this component.

Author:
    Rohan Khayech

License Terms and Copyright:
    Copyright (C) 2021 Rohan Khayech

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
import os
from typing import List

from astropy.coordinates import SkyCoord
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase, MySQLCursor

from model.report_types import ImportedReport, ReportResult
from model.search_filters import SearchFilters
from model.alias_result import AliasResult

# Public functions
def get_hashed_password(username:str)->str:
    """
    Retrieves the stored hashed password for the specified user if the user exists.

    Args:
        username (str): The admin username to lookup.

    Returns:
        str: The stored hashed password.

    Raises:
        UserNotFoundError: When the specified user is not found in the database. This can be avoided by calling the userExists() method beforehand.
    """
    # Connect to mysql server
    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    query = ("select passwordHash from AdminUsers where username = %s")

    cur.execute(query, (username,))
    result = cur.fetchone()
    
    if result is not None:
        return result[0]
    else:
        raise UserNotFoundError()

def user_exists(username:str)->bool:
    """
    Checks if an admin user with the specified username exists in the database.

    Args:
        username (str): The admin username to lookup.

    Returns:
        bool: True if the user was found, False otherwise.
    """
    # Connect to mysql server
    cn = _connect()
    cur:MySQLCursor = cn.cursor()

    query = ("select username from AdminUsers where username = %s")
    
    cur.execute(query,(username,))

    if cur.fetchone() == None:
        return False
    else:
        return True

def add_admin_user(username:str, password:str):
    """
    Stores a new admin user with the specified username and password if the user does not already exist.

    Args:
        username (str): The unique username of the admin user to add.
        password (str): The hashed password of the admin user to add.

    Raises:
        ExistingUserError: When the specified username is already associated with another user stored in the database. The new user cannot be added.
    """
    cn = _connect()
    cur:MySQLCursor = cn.cursor()

    query = ("insert into AdminUsers "
            "(username, passwordHash) "
            "values (%s, %s)")

    data = (username, password)

    try:
        cur.execute(query, data)
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_DUP_ENTRY:
            raise ExistingUserError()
        else:
            raise e
    finally:
        cn.commit()
        cur.close()
        cn.close()

def add_report(report:ImportedReport):
    """
    Stores a new report in the database with all the fields specified in the given report object. This method also creates relational records between reports and objects, related reports and coordinates.

    Args:
        report (ImportedReport): The report to be stored in the database.

    Raises:
        ExistingReportError: When the ATel number of the specified report is already associated with a report stored in the database.
    """
    pass #stub

def report_exists(atel_num:int)->bool:
    """
    Checks whether a report with the specified ATel number is stored in the database.

    Args:
        atel_num (int): The ATel number of the report to lookup.

    Returns:
        bool: True if the report was found, False otherwise.
    """
    return False

def get_all_aliases()->list[AliasResult]:
    """
    Retrieves a list of all object aliases stored in the database and their associated object IDs.

    Returns:
        list[AliasResult]: A list of AliasResult objects, containing aliases and their associated object ID, or None if no aliases are stored.
    """
    return [AliasResult("example","x")] #stub

def get_next_atel_num()->int:
    """
    Retrieves the number of the next ATel report to start auto import from. This is equal to the last ATel number added to the database via the auto import function plus one. If no reports have been auto imported, this will be equal to one.

    Returns:
        int: The number of the next ATel report to start auto import from.
    """
    return 1 #stub

def set_next_atel_num(nextNum:int):
    """
    Sets the number of the next ATel report to start auto import from. This method should be called after the auto import function has finished.

    Args:
        nextNum (int): The number of the next ATel report to start auto import from. Should be equal to the last ATel number imported via auto import plus one.
    """
    pass

def get_last_updated_date()->datetime:
    """
    Retrieves the date that the database was updated with the latest ATel reports.

    Returns:
        datetime: The date the database was last updated with the latest ATel reports.
    """
    return datetime(2021,7,30) #stub

def add_object(object_id:str, coords:SkyCoord, aliases:list[str]):
    """
    Stores a new celestial object with the specified coordinates and it’s known aliases in the database.

    Args:
        object_id (str): The object’s main ID from SIMBAD.
        coords (SkyCoord): The object's coordinates.
        aliases (list[str]): list of strings representing alternative IDs/aliases for the object.

    Raises:
        ExistingObjectError: When the specified object ID is already associated with an object stored in the database.
    """
    pass

def add_aliases(object_id:str, aliases:list[str]):
    """
    Adds the specified aliases to the given stored object.

    Args:
        object_id (str): The object’s main ID from SIMBAD.
        aliases (list[str]): A list of strings representing alternative ID’s/aliases to add for the specified object.

    Raises:
        ObjectNotFoundError: Raised when the specified object ID is not stored in the database.
    """
    pass

def get_object_coords(alias:str)->SkyCoord:
    """
    Retrieves the coordinates of the stored celestial object with the specified alias.

    Args:
        alias (str): The alias to lookup.

    Returns:
        SkyCoord: The celestial object’s coordinates.

    Raises:
        ObjectNotFoundError: Raised when the specified alias is not stored in the database.
    """
    return SkyCoord(0.0,0.0)

def find_reports_by_object(filters:SearchFilters, object_name:str=None)->list[ReportResult]:
    """
    Queries the local database for reports matching the specified search filters and related to the specified object if given.

    Args:
        filters (SearchFilters): The search criteria to filter the report query with.
        object_name (str, optional): An object ID or alias to search  by. Defaults to None.

    Returns:
        list[ReportResult]: A list of reports matching all the search criteria and related to the specified object, or None if no matching reports where found.
    """
    return None #stub

def find_reports_in_coord_range(filters:SearchFilters, coords:SkyCoord, radius:int)->List[ReportResult]:
    """
    Queries the local database for reports matching the specified search filters and related to the specified object if given.

    Args:
        filters (SearchFilters): The search criteria to filter the report query with.
        coords (SkyCoord): The coordinates to search around.
        radius (int): The radius defining the range around the specified coordinates to search.

    Returns:
        list[ReportResult]: A list of reports matching all the search criteria and related to the specified object, or None if no matching reports where found.
    """
    return None # stub


def init_db():
    """
    Connects to the database and creates the schema if not already created.
    """
    # Connect to mysql server
    cn = _connect()
    cur = cn.cursor()

    # Load table schema from file
    user_table = open(os.path.join("..","model","schema","AdminUsers.sql")).read()

    # Add tables
    try:
        cur.execute(user_table)
    except mysql.connector.Error as err:
        print(err.msg)

    # Close connection
    cur.close()
    cn.close()

# Exceptions
class ExistingUserError(Exception):
    """
    Raised when the specified username is already associated with another user stored in the database.
    """

class UserNotFoundError(Exception):
    """
    Raised when the specified user is not found in the database.
    """

# Private functions
def _link_reports(object_id:str, aliases:List[str]):
    """
    Adds records relating reports and the specified object ID, where the report contains one or more of the specified aliases.

    Args:
        object_id (str): The object’s main ID from SIMBAD.
        aliases (list[str]): List of strings representing new alternative ID’s/aliases to search for in reports.

    Raises:
        ObjectNotFoundError: Raised when the specified object ID is not stored in the database.
    """
    pass

def _connect()->MySQLConnection:
    """
    Connects to the MySQL server and database and returns the connection object.

    Returns:
        MySQLConnection: Connection to the MySQL Server. Must be closed by the calling method once finished. 
    """
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"), 
        user=os.getenv("MYSQL_USER"), 
        password=os.getenv("MYSQL_PASSWORD"), 
        database=os.getenv("MYSQL_DB")
    )
