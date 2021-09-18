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
from datetime import date, datetime
import os

from astropy.coordinates import SkyCoord
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from model.ds.report_types import ImportedReport, ReportResult
from model.ds.search_filters import SearchFilters, DateFilter, KeywordMode
from model.ds.alias_result import AliasResult
from controller.helper.type_checking import list_is_type

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

    cn = _connect()
    try:
        # Execute query and handle errors
        cur:MySQLCursor = cn.cursor()
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
            
        # Add object relations
        object_ref_query = ("insert into ObjectRefs"
                            "(atelNumFK, objectIDFK) "
                            "values (%s, %s)")
        cur: MySQLCursor = cn.cursor()
        for object_id in report.objects:
            try:  
                object_ref_data = (report.atel_num, object_id)
                cur.execute(object_ref_query, object_ref_data)
                
            except mysql.connector.Error as e:
                raise e
            finally:
                cn.commit()
                cur.close()

            #TODO: Add observation dates.
            #TODO: Convert and add coordinates.
            #TODO: Add referenced reports/by.
    except mysql.connector.Error as e:
        raise e
    finally:
        cn.close()


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
        list[AliasResult]: A list of AliasResult objects, containing aliases and their associated object ID.
    """
    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    query = "select alias, objectIDFK from Aliases"

    aliases = []

    try:
        cur.execute(query)
        for row in cur.fetchall():
            #extract data
            atel_num:int = row[0]
            object_ID:str = row[1]
            
            #create result object and add to list
            alias_result = AliasResult(atel_num,object_ID)
            aliases.append(aliases)
    except mysql.connector.Error as e:
        raise e
    finally:
        cur.close()
        cn.close()

    if len(aliases) == 0:
        return None
    else:
        return aliases


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
        object_id (str): The object’s main ID from SIMBAD. (Max 255 chars)
        coords (SkyCoord): The object's coordinates.
        aliases (list[str]): list of strings representing alternative IDs/aliases for the object.

    Raises:
        ExistingObjectError: When the specified object ID is already associated with an object stored in the database.
    """
    # Type conversion/check
    object_id = str(object_id)
    if ((type(coords) is not SkyCoord) or (not list_is_type(aliases,str))):
        raise TypeError("Invalid coords or list of aliases.")

    # Check length is valid
    if len(object_id) in range(1, 256):
        # connect to database
        cn = _connect()
        cur: MySQLCursor = cn.cursor()

        # setup query
        query = ("insert into Objects" 
                " (objectID, ra, declination)" 
                " values (%s, %s, %s)")

        data = (object, SkyCoord.ra.deg.item(), SkyCoord.dec.deg.item())

        # execute query and handle errors
        try:
            cur.execute(query, data)
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise ExistingObjectError()
            else:
                raise e
        finally:
            cn.commit()
            cur.close()
            cn.close()
    else:
        raise ValueError(
            "Specified object_id must be valid lengths and non-empty."
        )

    # Add aliases
    add_aliases(object_id,aliases)


def add_aliases(object_id: str, aliases: list[str]):
    """
    Adds the specified aliases to the given stored object.

    Args:
        object_id (str): The object’s main ID from SIMBAD.
        aliases (list[str]): A list of strings representing alternative ID’s/aliases to add for the specified object.

    Raises:
        ObjectNotFoundError: Raised when the specified object ID is not stored in the database. 
    """
    # Type conversion/check
    object_id = str(object_id)
    
    # Check length is valid
    if len(object_id) in range(1, 256):
        if object_exists(object_id):
            # connect to database
            cn = _connect()
            cur: MySQLCursor = cn.cursor()

            # setup query
            query = ("insert into Aliases"
                    " (alias, objectIDFK)"
                    " values (%s, %s);")

            for alias in aliases:
                data = (object_id,alias)

                # execute query and handle errors
                try:
                    cur.execute(query, data)
                except mysql.connector.Error as e:
                    if e.errno == errorcode.ER_DUP_ENTRY:
                        pass #ignore any duplicate aliases
                    else:
                        raise e
                finally:
                    cn.commit()
                    cur.close()
                    cn.close()
        else:
            raise ObjectNotFoundError("The specified object ID is not stored in the database.")
    else:
        raise ValueError(
            "Specified object_id must be valid lengths and non-empty."
        )



def object_exists(alias:str)->tuple[bool,datetime]:
    """
    Checks whether an object with the specified alias exists in the database.

    Args:
        alias (str): The alias to lookup.

    Returns:
        bool: True if an object with the specified alias exists, false otherwise.
        datetime: The date the specified object was last updated via SIMBAD, or None if no object exists.
    """
    query = ("select lastUpdated from Objects"
             " where objectID = %s")
    
    try: 
        object_id = _get_object_id(alias)
    except (ObjectNotFoundError):
        return False, None

    cn = _connect()
    cur: MySQLCursor = cn.cursor()
    cur.execute(query, (object_id,))

    result = cur.fetchone()

    if result:
        lastUpdated = result[0]
        return True, lastUpdated
    else:
        return False, None

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
    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    query = ("select ra, declination from Objects"
             " where objectID = %s")

    cur.execute(query, (id,))

    result = cur.fetchone()

    if result:
        ra = result[0]
        dec = result[1]
        return SkyCoord(ra, dec, frame='icrs', unit=('hourangle', 'deg'))
    else:
        raise ObjectNotFoundError("The specified object ID is not stored in the database.")


def find_reports_by_object(filters: SearchFilters = None, date_range: DateFilter = None, object_name: str = None) -> list[ReportResult]:
    """
    Queries the local database for reports matching the specified search filters and related to the specified object if given.

    Args:
        filters (SearchFilters, optional): The search criteria to filter the report query with. Defaults to None.
        date_range (DateFilter, optional): The date range to filter the report query by. Defaults to None.
        object_name (str, optional): An object ID or alias to search  by. Defaults to None.

    Returns:
        list[ReportResult]: A list of reports matching all the search criteria and related to the specified object.
    """
    if (filters is None):
        return [] #stubbed until object search is implemented

    if (filters or object_name):
        cn = _connect()
        cur:MySQLCursor = cn.cursor()

        query, data = _build_report_name_query(filters, date_range, object_name)

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
    else: # If no parameters given, return empty list.
        return []

def find_reports_in_coord_range(filters:SearchFilters, date_range: DateFilter, coords:SkyCoord, radius:float)->list[ReportResult]:
    """
    Queries the local database for reports matching the specified search filters and related to the specified object if given.

    Args:
        filters (SearchFilters): The search criteria to filter the report query with.
        date_range (DateFilter, optional): The date range to filter the report query by. Defaults to None.
        coords (SkyCoord): The coordinates to search around.
        radius (float): The radius defining the range around the specified coordinates to search.

    Returns:
        list[ReportResult]: A list of reports matching all the search criteria and related to the specified object.
    """
    return find_reports_by_object(filters, date_range) # stub

    #TODO: Check in coord range.

# Exceptions
class ExistingUserError(Exception):
    """
    Raised when the specified username is already associated with another user stored in the database.
    """

class ExistingReportError(Exception):
    """
    Raised when the ATel number of the specified report is already associated with a report stored in the database.
    """


class ExistingObjectError(Exception):
    """
    Raised when the specified object ID is already associated with an object stored in the database.
    """

class ExistingAliasError(Exception):
    """
    Raised when the specified object ID is already associated with an object stored in the database.
    """

class UserNotFoundError(Exception):
    """
    Raised when the specified user is not found in the database.
    """

class ObjectNotFoundError(Exception):
    """
    Raised when the specified object ID is not stored in the database.
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
    cn = _connect()
    cur:MySQLCursor = cn.cursor()

    reports:list[int] = []

    #query to find all reports with alias in body or title
    find_query = ("select atel_num"
            " from Reports"
            " where title like concat('%', %s, '%')"
            " or body like concat('%', %s, '%');")

    add_query = ("insert into ObjectRefs"
                " (atelNumFK, objectIDFK)"
                " values (%s,%s);")

    if (object_exists(object_id)):
        try:
            #loop through every alias
            for alias in aliases:
                find_data = (alias, alias)
                
                cur.execute(find_query, find_data)
                for row in cur.fetchall():
                    #extract data
                    atel_num = row[0]
                    #add to list of reports to link
                    reports.append(atel_num)

            #TODO: link by coords? This is in SRS but not specified where implemented in SAS.

            #loop through each report found and add a record relating it to the specified object
            for atel_num in reports:
                add_data = (atel_num, object_id)
                cur.execute(add_query, add_data)
        except mysql.connector.Error as e:
            raise e
        finally:
            cur.close()
            cn.close()
    else:
        raise ObjectNotFoundError("The specified object ID is not stored in the database.")


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

def _build_report_base_query()->str:
    """
    Builds the base query SQL query to select reports.

    Returns:
        str: The SQL query.
    """

    # Define base Select from Reports query
    base_query = ("select atelNum, title, authors, body, submissionDate"
            " from Reports"
            " where ")

    return base_query


def _build_report_name_query(filters: SearchFilters = None, date_range: DateFilter = None, object_name: str = None):
    """
    Builds the SQL query to select reports based on the specified search filters and/or object name.

    Args:
        filters (SearchFilters, optional): A valid search filters object to build the query with.
        date_filters (DateFilters, optional): A valid search filters object to build the query with. Defaults to None.

    Returns:
        str: The SQL where clause.
        tuple: The data to inject into the query on execution. 
    """

    #Build query clauses.
    base_query = _build_report_base_query()
    join_clause, join_data = _build_join_clause(object_name)
    where_clause, where_data = _build_where_clause(filters, date_range)

    # Build final query and compile data
    query = base_query + join_clause + where_clause
    data = join_data + where_data

    return query, data

def _build_where_clause(filters: SearchFilters = None, date_range: DateFilter = None)->tuple[str,tuple]:
    """
    Builds the where clause of the SQL query to select reports based on the specified search filters.

    Args:
        filters (SearchFilters, optional): A valid search filters object to build the query with.
        date_filters (DateFilters, optional): A valid search filters object to build the query with. Defaults to None.

    Returns:
        str: The SQL where clause.
        tuple: The data to inject into the query on execution. 
    """
    
    # Start with empty lists of terms and data
    data = ()
    clauses = []

    if date_range:
        # Append date clauses and data
        if date_range.start_date:
            clauses.append("submissionDate >= %s ")
            data = data + (date_range.start_date,)

        if date_range.end_date:
            clauses.append("submissionDate <= %s ")
            data = data + (date_range.end_date,)

    if filters:
        # Append term clause and data
        if filters.term:
            clauses.append(
                "(title like concat('%', %s, '%') or body like concat('%', %s, '%')) ")
            data = data + (filters.term, filters.term)

        # Append keyword clauses and data
        if filters.keywords:
            kw_clauses = []
            if filters.keyword_mode == KeywordMode.NONE:
                # Add a clause for each keyword in filters to not be in set
                for kw in filters.keywords:
                    kw_clauses.append("FIND_IN_SET(%s, keywords) = 0")  # If kw not in set
                    data = data + (kw,)
                kw_sep = " and "
            else:
                # Append a clause for each keyword to be in set
                for kw in filters.keywords:
                    kw_clauses.append("FIND_IN_SET(%s, keywords) > 0")  # If kw in set.
                    data = data + (kw,)

                # Set or/and condition
                if filters.keyword_mode == KeywordMode.ALL:
                    kw_sep = " and "
                elif filters.keyword_mode == KeywordMode.ANY:
                    kw_sep = " or "
            # Join keyword clauses into one clause
            kw_clause = "(" + kw_sep.join(kw_clauses)+") "
            clauses.append(kw_clause)

    # Join where clauses together
    sep = "and "
    where_clause = sep.join(clauses)

    return where_clause, data

def _build_join_clause(object_name:str = None)->tuple[str,tuple]:
    """
    Builds the join clause of the SQL query to select reports linked to the specified object.

    Args:
        object_name (str, optional): An object ID or alias to search by. Defaults to None.

    Returns:
        str: The SQL join clause.
        tuple: The data to inject into the query on execution. 

    Raises:
        ObjectNotFoundError: When an object with the given alias is not stored in the database.

    """
    if object_name:
        object_id = _get_object_id(object_name)

        join_clause = ("right join ObjectRefs"
                       "on Reports.atelNum = ObjectRefs.atelNumFK"
                       "and ObjectRefs.objectIDFK = %s")
        
        join_data = (object_id,)
    else:
        join_clause = ""
        join_data = ()

    return join_clause, join_data

def _get_object_id(alias:str)->str:
    """
    Finds the main object ID that the given alias refers to.

    Args:
        alias (str): The alias to lookup.

    Returns:
        str: The object's main ID from SIMBAD.

    Raises:
        ObjectNotFoundError: When an object with the given alias is not stored in the database.
    """
    query = ("select objectIDFK "
             "from Aliases "
             "where alias like '%s'"
             "or objectIDFK like '%s'")

    cn = _connect()
    cur:MySQLCursor = cn.cursor()

    try:
        cur.execute(query, (alias,alias))
        result = cur.fetchone()

        if result is None:
            raise ObjectNotFoundError()
        else:
            object_id = result[0]
    except mysql.connector.Error as e:
        raise e
    finally:
        cur.close()
        cn.close()

    return object_id
