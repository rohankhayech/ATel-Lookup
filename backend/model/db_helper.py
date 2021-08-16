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

from astropy.coordinates import SkyCoord
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase, MySQLCursor

from model.constants import FIXED_KEYWORDS
from model.ds.report_types import ImportedReport, ReportResult
from model.ds.search_filters import SearchFilters
from model.ds.alias_result import AliasResult

# Public functions
def get_hashed_password(username: str) -> str:
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

    query = "select passwordHash from AdminUsers where username = %s"

    cur.execute(query, (username,))
    result = cur.fetchone()

    if result is not None:
        return result[0]
    else:
        raise UserNotFoundError()

def user_exists(username: str) -> bool:
    """
    Checks if an admin user with the specified username exists in the database.

    Args:
        username (str): The admin username to lookup.

    Returns:
        bool: True if the user was found, False otherwise.
    """
    return _record_exists("AdminUsers", "username", username)

def add_admin_user(username: str, password: str):
    """
    Stores a new admin user with the specified username and password if the user does not already exist.

    Args:
        username (str): The unique username of the admin user to add. Max 24 chars.
        password (str): The hashed password of the admin user to add. Max 255 chars.

    Raises:
        ExistingUserError: When the specified username is already associated with another user stored in the database. The new user cannot be added.
        ValueError: When username or password are empty strings or exceed the specified max lengths.
    """
    # Type conversion
    username = str(username)
    password = str(password)

    # Check length is valid
    if len(username) in range(1, 25) and len(password) in range(1, 255):
        # connect to database
        cn = _connect()
        cur: MySQLCursor = cn.cursor()

        # setup query
        query = "insert into AdminUsers" " (username, passwordHash)" " values (%s, %s)"

        data = (username, password)

        # execute query and handle errors
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
    else:
        raise ValueError(
            "Specified username and password must be valid lengths and non-empty."
        )


def add_report(report: ImportedReport):
    """
    Stores a new report in the database with all the fields specified in the given report object. This method also creates relational records between reports and objects, related reports and coordinates.

    Args:
        report (ImportedReport): The report to be stored in the database.

    Raises:
        ExistingReportError: When the ATel number of the specified report is already associated with a report stored in the database.
    """
    cn = _connect()
    cur:MySQLCursor = cn.cursor()

    # Format keywords
    sep = ','
    keywords = sep.join(report.keywords)  
    sub_date = report.submission_date.strftime("%Y-%m-%d %H:%M:%S")

    report_query = ("insert into Reports "
                    "(atelNum, title, authors, body, submissionDate, keywords) "
                    "values (%s, %s, %s, %s, %s, %s)")

    data = (report.atel_num, report.title, report.authors, report.body, sub_date, keywords)

    metadata_query = ("update Metadata "
                      "set lastUpdatedDate = CURDATE()")                

    #execute query and handle errors
    try:
        cur.execute(report_query, data)
        cur.execute(metadata_query)
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_DUP_ENTRY:
            raise ExistingReportError()
        else:
            raise e
    finally:
        cn.commit()
        cur.close()
        cn.close()

    #TODO: Add objects.
    #TODO: Add observation dates.
    #TODO: Convert and and coordinates.
    #TODO: Add referenced reports/by. 


def report_exists(atel_num: int) -> bool:
    """
    Checks whether a report with the specified ATel number is stored in the database.

    Args:
        atel_num (int): The ATel number of the report to lookup.

    Returns:
        bool: True if the report was found, False otherwise.
    """
    return _record_exists("Reports","atelNum",atel_num)


def get_all_aliases() -> list[AliasResult]:
    """
    Retrieves a list of all object aliases stored in the database and their associated object IDs.

    Returns:
        list[AliasResult]: A list of AliasResult objects, containing aliases and their associated object ID, or None if no aliases are stored.
    """
    return [AliasResult("example", "x")]  # stub


def get_next_atel_num() -> int:
    """
    Retrieves the number of the next ATel report to start auto import from. This is equal to the last ATel number added to the database via the auto import function plus one. If no reports have been auto imported, this will be equal to one.

    Returns:
        int: The number of the next ATel report to start auto import from.
    """
    cn = _connect()
    cur:MySQLCursor = cn.cursor()

    query = "select nextATelNum from Metadata"

    try:
        #Add single metadata entry
        cur.execute(query)
        result = cur.fetchone()

        next_atel_num = result[0]
    except mysql.connector.Error as e:
        raise e
    finally:
        cur.close()
        cn.close()

    return next_atel_num

def set_next_atel_num(nextNum: int):
    """
    Sets the number of the next ATel report to start auto import from. This method should be called after the auto import function has finished.

    Args:
        nextNum (int): The number of the next ATel report to start auto import from. Should be equal to the last ATel number imported via auto import plus one.
    """
    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    query = ("update Metadata "
             "set nextATelNum = %s")

    try:
        cur.execute(query, (nextNum,))
    except mysql.connector.Error as e:
        raise e
    finally:
        cn.commit()
        cur.close()
        cn.close()


def get_last_updated_date() -> datetime:
    """
    Retrieves the date that the database was updated with the latest ATel reports.

    Returns:
        datetime: The date the database was last updated with the latest ATel reports.
    """
    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    query = "select lastUpdatedDate from Metadata"

    try:
        cur.execute(query)
        result = cur.fetchone()

        date = result[0]
    except mysql.connector.Error as e:
        raise e
    finally:
        cur.close()
        cn.close()

    return date


def add_object(object_id: str, coords: SkyCoord, aliases: list[str]):
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


def add_aliases(object_id: str, aliases: list[str]):
    """
    Adds the specified aliases to the given stored object.

    Args:
        object_id (str): The object’s main ID from SIMBAD.
        aliases (list[str]): A list of strings representing alternative ID’s/aliases to add for the specified object.

    Raises:
        ObjectNotFoundError: Raised when the specified object ID is not stored in the database.
    """
    pass


def get_object_coords(alias: str) -> SkyCoord:
    """
    Retrieves the coordinates of the stored celestial object with the specified alias.

    Args:
        alias (str): The alias to lookup.

    Returns:
        SkyCoord: The celestial object’s coordinates.

    Raises:
        ObjectNotFoundError: Raised when the specified alias is not stored in the database.
    """
    return SkyCoord(0.0, 0.0)


def find_reports_by_object(
    filters: SearchFilters, object_name: str = None
) -> list[ReportResult]:
    """
    Queries the local database for reports matching the specified search filters and related to the specified object if given.

    Args:
        filters (SearchFilters): The search criteria to filter the report query with.
        object_name (str, optional): An object ID or alias to search  by. Defaults to None.

    Returns:
        list[ReportResult]: A list of reports matching all the search criteria and related to the specified object, or None if no matching reports where found.
    """
    cn = _connect()
    cur:MySQLCursor = cn.cursor()

    query = ("select atelNum, title, authors, body, submissionDate"
             " from Reports"
             " where title = %s")

    data = (filters.term,)

    reports = []

    try:
        cur.execute(query, data)
        for row in cur.fetchall():
            #extract data
            atel_num = row[0]
            title = row[1]
            authors = row[2]
            body = row[3]
            submission_date = row[4]

            #create result object and add to list
            report = ReportResult(atel_num,title,authors,body,submission_date)
            reports.append(report)
    except mysql.connector.Error as e:
        raise e
    finally:
        cur.close()
        cn.close()

    return reports
def find_reports_in_coord_range(filters:SearchFilters, coords:SkyCoord, radius:int)->list[ReportResult]:
    """
    Queries the local database for reports matching the specified search filters and related to the specified object if given.

    Args:
        filters (SearchFilters): The search criteria to filter the report query with.
        coords (SkyCoord): The coordinates to search around.
        radius (int): The radius defining the range around the specified coordinates to search.

    Returns:
        list[ReportResult]: A list of reports matching all the search criteria and related to the specified object, or None if no matching reports where found.
    """
    return None  # stub


def init_db():
    """
    Connects to the database and creates the schema if not already created.
    """
    # Connect to mysql server
    cn = _connect()
    cur:MySQLCursor = cn.cursor()

    # Load table schema from file
    user_table = _read_table("AdminUsers")
    reports_table = _read_table("Reports")
    metadata_table = _read_table("Metadata")

    # Add keywords to reports schema
    sep = "', '"
    kw_set = sep.join(FIXED_KEYWORDS)
    reports_table = reports_table.format(kw_set)
   
    try:
        # Add tables
        cur.execute(user_table)
        cur.execute(reports_table)
        cur.execute(metadata_table)

        #Add single metadata entry
        cur.execute("insert into Metadata (metadata) values ('metadata');")
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        # Close connection
        cn.commit()
        cur.close()
        cn.close()


# Exceptions
class ExistingUserError(Exception):
    """
    Raised when the specified username is already associated with another user stored in the database.
    """
class ExistingReportError(Exception):
    """
    When the ATel number of the specified report is already associated with a report stored in the database.
    """


class UserNotFoundError(Exception):
    """
    Raised when the specified user is not found in the database.
    """


# Private functions
def _link_reports(object_id: str, aliases: list[str]):
    """
    Adds records relating reports and the specified object ID, where the report contains one or more of the specified aliases.

    Args:
        object_id (str): The object’s main ID from SIMBAD.
        aliases (list[str]): List of strings representing new alternative ID’s/aliases to search for in reports.

    Raises:
        ObjectNotFoundError: Raised when the specified object ID is not stored in the database.
    """
    pass


def _connect() -> MySQLConnection:
    """
    Connects to the MySQL server and database and returns the connection object.

    Returns:
        MySQLConnection: Connection to the MySQL Server. Must be closed by the calling method once finished.
    """
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
    )

def _read_table(table_name:str)->str:
    """Reads schema for the given table from it's SQL file.

    Args:
        table_name (str): The name of the table to import.

    Returns:
        str: The SQL schema for the given table.
    """
    schema_path = os.path.join("model", "schema", f"{table_name}.sql")
    return open(schema_path).read()

def _record_exists(table_name:str,primary_key:str,id:str)->bool:
    """
    Checks if the given record exists.

    Args:
        table_name (str): Name of the table.
        primary_key (str): Primary key of the table.
        id (str): ID of the record to check.
    """
    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    query = (f"select count(*) from {table_name}"
             f" where {primary_key} = %s")

    cur.execute(query, (id,))

    result = cur.fetchone()

    if result[0] >= 1:
        return True
    else:
        return False
