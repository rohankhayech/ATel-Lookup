from datetime import datetime
from typing import List
from astropy.coordinates import SkyCoord

# Public functions
def import_report(atel_num: int):
    """
    Adds new ATel report to the database if it is valid.

    Args:
        atel_num (int): The ATel number of the new report to be added.

    Raises:
        ReportAlreadyExistsException: Thrown when report with the ATel number has been added to the database previously.
        ReportNotFoundException: Thrown when report with the ATel number is not found on the AT website.
    """
    pass

def import_all_reports():
    """
    Adds all new ATel reports to the database starting after the last ATel report imported.
    """
    pass

# Private functions
def download_report(atel_num: int) -> str:
    """
    Downloads the HTML of ATel report.

    Args:
        atel_num (int): The ATel number of the report to be downloaded.

    Returns:
        str: String representation of the downloaded HTML.

    Raises:
        NetworkErrorException: Thrown when network failure occurs during the HTML download.
        DownloadFailException: Thrown when the HTML could not be downloaded.
    """
    return ''

def parse_report(html_string: str) -> ImportedReport:
    """
    Extracts data from ATel report as stated in non-functional requirement 1 in the SRS.

    Args:
        html_string (str): String representation of the downloaded HTML of ATel report from which to extract data from.

    Returns:
        ImportedReport: Object containing all extracted data from the ATel report.

    Raises:
        MissingReportElementException: Thrown when important data could not be extracted or are missing from the report.
    """
    return ImportedReport(1, '', '', '', datetime(2000, 1, 1), [], [], [], [], [], [])

def extract_coords(body_text: str) -> list[str]:
    """
    Finds all coordinates in the body text of ATel report.

    Args:
        body_text (str): Body text of ATel report.

    Returns:
        list[str]: List of coordinates found.
    """
    return []

def parse_coords(coords: list[str]) -> list[SkyCoord]:
    """
    Parse coordinates that were found into appropriate format so that they can be used to query SIMBAD.

    Args:
        coords (list[str]): List of coordinates found in the body text of ATel report.

    Returns:
        list[SkyCoord]: List of formatted coordinates.
    """
    return []

def extract_dates(body_text: str) -> list[str]:
    """
    Finds all dates in the body text of ATel report.

    Args:
        body_text (str): Body text of ATel report.

    Returns:
        list[str]: List of dates found.
    """
    return []

def parse_dates(dates: list[str]) -> list[datetime]:
    """
    Parse dates that were found into datetime objects so that they can be inserted easily to the database.

    Args:
        dates (list[str]): List of dates found in the body text of ATel report.

    Returns:
        list[datetime]: List of datetime objects representing dates.
    """
    return []

def extract_known_aliases(body_text: str) -> list[str]:
    """
    Finds all known aliases in the body text of ATel report.

    Args:
        body_text (str): Body text of ATel report.

    Returns:
        list[str]: List of known aliases found.
    """
    return []

def extract_keywords(body_text: str) -> list[str]:
    """
    Finds all keywords in the body text of ATel report.

    Args:
        body_text (str): Body text of ATel report.

    Returns:
        list[str]: List of keywords found.
    """
    return []
