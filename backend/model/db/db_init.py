"""
The database initializer handles creating, checking and upgrading the database schema.
This represents part of the database interface.

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
import os
import warnings

import mysql.connector
from mysql.connector.cursor import MySQLCursor

from model.constants import FIXED_KEYWORDS
from model.db.db_interface import _connect

# Constants

_LATEST_SCHEMA_VERSION: int = 7
""" 
Version number of the latest database schema.
This must be increased every time the schema is upgraded.
"""

_LATEST_SCHEMA_VERSION_REQUIRES_RESET: bool = False
"""
Flag indiciating whether the database requires a hard reset to upgrade.
This should only be set to True if the database cannot be altered using SQL.
"""

# Public Functions

def init_db():
    """
    Initializes the database, creating/upgrading it if needed.
    """
    # Check schema version
    schema_version = _get_schema_version()
    if (schema_version is None):  # Database does not yet exist.
        # Create db from schema
        _create_db()
    # Database schema is previous version.
    elif (schema_version == _LATEST_SCHEMA_VERSION-1):
        if _LATEST_SCHEMA_VERSION_REQUIRES_RESET:
            _warn_schema_incompatible(schema_version)
        else:
            # Create any new tables added.
            _create_db()
            # Alter existing tables
            _upgrade_db(schema_version)
    # Database schema is an older/newer version.
    elif (schema_version != _LATEST_SCHEMA_VERSION):
        _warn_schema_incompatible(schema_version)


# Exceptions

class IncompatibleSchemaVersionWarning(Warning):
    """
    Raised when the schema version is incompatible with the latest version and must be reset to be upgraded.
    """


class SchemaUpgradedWarning(Warning):
    """
    Raised when the schema version has been upgraded.
    """


# Private methods

def _read_table(table_name: str) -> str:
    """
    Reads schema for the given table from it's SQL file.

    Args:
        table_name (str): The name of the table to import.

    Returns:
        str: The SQL schema for the given table.
    """
    schema_path = os.path.join("model", "schema", f"{table_name}.sql")
    return _read_schema(schema_path)


def _read_table_upgrade(table_name: str) -> str:
    """
    Reads schema to for upgrading the given table from it's SQL file.

    Args:
        table_name (str): The name of the table to import.

    Returns:
        str: The SQL schema for the given table.
    """
    schema_path = os.path.join("model", "schema", "upgrade", f"upgrade_{table_name}.sql")
    return _read_schema(schema_path)


def _read_schema(file_path: str) -> str:
    """
    Reads schema for the given table from it's SQL file.

    Args:
        table_name (str): The name of the table to import.

    Returns:
        str: The SQL schema for the given table.
    """
    return open(file_path).read()


def _create_db():
    """
    Connects to the database and creates the schema if not already created.
    """
    # Connect to mysql server
    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    # Load table schema from file
    user_table = _read_table("AdminUsers")
    reports_table = _read_table("Reports")
    metadata_table = _read_table("Metadata")
    objects_table = _read_table("Objects")
    object_refs_table = _read_table("ObjectRefs")
    aliases_table = _read_table("Aliases")
    report_refs_table = _read_table("ReportRefs")
    report_coords_table = _read_table("ReportCoords")
    ob_dates_table = _read_table("ObservationDates")

    # Add keywords to reports schema
    sep = "', '"
    kw_set = sep.join(FIXED_KEYWORDS)
    reports_table = reports_table.format(kw_set)

    try:
        # Add tables
        cur.execute(user_table)
        cur.execute(reports_table)
        cur.execute(metadata_table)
        cur.execute(objects_table)
        cur.execute(object_refs_table)
        cur.execute(aliases_table)
        cur.execute(report_refs_table)
        cur.execute(report_coords_table)
        cur.execute(ob_dates_table)

        #Add single metadata entry
        cur.execute(
            "insert into Metadata (metadata, schemaVersion) values ('metadata', %s);", (_LATEST_SCHEMA_VERSION,))
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        # Close connection
        cn.commit()
        cur.close()
        cn.close()


def _upgrade_db(old_schema_version: int):
    """
    Upgrades the database to the next version using the upgrade schema.
    Should only be called if the schema was the previous version.

    Args:
        old_schema_version (int): The schema version to upgrade from.
    """

    # Connect to mysql server
    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    # Load table upgrade schema from file
    user_table = _read_table_upgrade("AdminUsers")
    reports_table = _read_table_upgrade("Reports")
    metadata_table = _read_table_upgrade("Metadata")
    objects_table = _read_table_upgrade("Objects")
    object_refs_table = _read_table_upgrade("ObjectRefs")
    aliases_table = _read_table_upgrade("Aliases")
    report_refs_table = _read_table_upgrade("ReportRefs")
    report_coords_table = _read_table_upgrade("ReportCoords")
    ob_dates_table = _read_table_upgrade("ObservationDates")

    metadata_query = ("update Metadata "
                      "set schemaVersion = %s;")

    try:
        # Alter tables
        cur.execute(user_table)
        cur.execute(reports_table)
        cur.execute(metadata_table)
        cur.execute(objects_table)
        cur.execute(object_refs_table)
        cur.execute(aliases_table)
        cur.execute(report_refs_table)
        cur.execute(report_coords_table)
        cur.execute(ob_dates_table)

        #Update version
        cur.execute(metadata_query, (_LATEST_SCHEMA_VERSION,))

        _warn_schema_upgraded(old_schema_version)
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        # Close connection
        cn.commit()
        cur.close()
        cn.close()


def _get_schema_version() -> int:
    """
    Retrieves the version number of the current database schema.

    Returns:
        int: Version number of the current schema or None if the database is not created.
    """

    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    # Check if the database was created.
    cur.execute(f"show tables like 'Metadata';")
    exists_result = cur.fetchone()

    # If the database is not created return none.
    if exists_result is None:
        return None

    query = "select schemaVersion from Metadata"

    try:
        cur.execute(query)
        result = cur.fetchone()

        ver = result[0]
    except mysql.connector.Error as e:
        raise e
    finally:
        cur.close()
        cn.close()

    return ver


def _reset_db():
    """
    Resets and recreates the database.
    This should only be used if the current schema version is incompatible with the latest schema version.
    This should only be called from the console, do not call internally.
    
    WARNING: This function will DELETE ALL stored application data.
    """
    cn = _connect()
    cur: MySQLCursor = cn.cursor()

    try:
        cur.execute("drop table AdminUsers;")
        cur.execute("drop table Metadata;")
        cur.execute("drop table ObjectRefs;")
        cur.execute("drop table Aliases;")
        cur.execute("drop table ObservationDates;")
        cur.execute("drop table ReportCoords;")
        cur.execute("drop table ReportRefs;")
        cur.execute("drop table Reports;")
        cur.execute("drop table Objects;")
    except mysql.connector.Error as err:
        print(err.msg)
    finally:
        # Close connection
        cn.commit()
        cur.close()
        cn.close()

    _create_db()


def _warn_schema_incompatible(schema_version: int):
    """
    Warns that the schema version is incompatible with the latest version.

    Args:
        schema_version (int): The current schema version.
    """
    msg = f"\n\nWARNING: Incompatible Schema Version:\nDatabase schema version v{schema_version} is incompatible with the latest schema version v{_LATEST_SCHEMA_VERSION} and cannot be upgraded automatically.\nDatabase must be reset by calling _reset_db().\nIMPORTANT NOTE: This will delete all stored application data.\nAllowing the application to continue without resetting the database could lead to unstable results.\n"
    warnings.warn(msg, IncompatibleSchemaVersionWarning)


def _warn_schema_upgraded(schema_version: int):
    """
    Warns that the schema version has been upgraded.

    Args:
        schema_version (int): The current schema version.
    """
    msg = f"Database schema upgraded from v{schema_version} to v{_LATEST_SCHEMA_VERSION}."
    warnings.warn(msg, SchemaUpgradedWarning)
