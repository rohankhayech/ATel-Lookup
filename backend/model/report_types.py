"""
Contains local data structures representing ATel reports imported and returned by the application.

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

from astropy.coordinates import SkyCoord

from helper.type_checking import list_is_type

class ReportResult:
    """
    An object representing a report returned from the local database as a result of a search query. Contains all the information needed for displaying the report as a search result and on both the timeline and network graphs.
    """

    def __init__(self, atel_num:int, title:str, authors:str, body:str, submission_date:datetime, referenced_reports:list[int]=[]):
        """
        Creates a ReportResult object with the specified fields.

        Args:
            atel_num (int): The ATel number associated with the report.
            title (str): The title of the report.
            authors (str): A string representing the authors of the report.
            body (str): The body text of the report. Must be <= 4000 characters.
            submission_date (datetime): A datetime object representing the date and time the report was submitted to The Astronomer's Telegram.
            referenced_reports (list[int], optional): List of ATel numbers of reports referenced by this report.
        """
        self.atel_num = atel_num
        self.title = title
        self.authors = authors
        self.body = body
        self.referenced_reports = referenced_reports
        self.submission_date = submission_date

    def __str__(self)->str:
        """
        Returns:
            str: A description of the report.
        """
        return f"ATel #{self.atel_num}: {self.title} ({self.authors}). Body length: {len(self.body)} chars. Submitted: {self.submission_date}. Referenced Reports: {self.referenced_reports}"

    @property
    def atel_num(self)->int:
        """
        The ATel number associated with the report.
        """
        return self._atel_num

    @atel_num.setter
    def atel_num(self, atel_num:int):
        """
        Sets the report's ATel number.

        Args:
            atel_num (int): A positive integer representing the ATel number associated with the report.

        Raises:
            ValueError: When the given ATel number is not a valid positive integer.
        """
        try:
            atel_num = int(atel_num)
        except ValueError:
            raise TypeError("ATel Number must be a valid positive integer.")

        if atel_num>0: #and atel_num<sys.maxint: - check int overflow in python?
            self._atel_num = atel_num
        else:
            raise ValueError("ATel Number must be a valid positive integer.")

    @property
    def title(self)->str:
        """
        The title of the report.
        """
        return self._title

    @title.setter
    def title(self, title:str):
        """
        Sets the title of the report.

        Args:
            title (str): The title of the report.
        """
        self._title = str(title)

    @property
    def authors(self)->str:
        """
        A string representing the authors of the report.
        """
        return self._authors

    @authors.setter
    def authors(self, authors:str):
        """Sets the authors of the report.

        Args:
            authors (str): A string representing the authors of the report.
        """
        self._authors = str(authors)

    @property
    def body(self)->str:
        """
        The body text of the report.
        """
        return self._body

    @body.setter
    def body(self, body:str):
        """
        Sets the body text of the report.

        Args:
            body (str): The body text of the report. Must be 4000 characters or less.

        Raises:
            ValueError: When the given body text exceeds 4000 characters.
        """
        body = str(body)

        if (len(body)<=4000):
            self._body = body
        else:
            raise ValueError("Body must be <= 4000 characters.")

    @property
    def submission_date(self)->datetime:
        """
        A Datetime object representing the date and time that the report was submitted to The Astronomer's Telegram.
        """
        return self._submission_date

    @submission_date.setter
    def submission_date(self, date:datetime):
        """
        Sets the submission date of the report.

        Args:
            date (datetime): A Datetime object representing the date and time that the report was submitted to The Astronomer's Telegram.
        """
        if type(date) == datetime:
            self._submission_date = date
        else: 
            raise TypeError("Submission date must be a valid datetime object.")

    @property
    def referenced_reports(self)->list[int]:
        """
        List of integers representing the ATel numbers of reports that this report references. 
        """
        return self._referenced_reports.copy()

    @referenced_reports.setter
    def referenced_reports(self, reports:list[int]):
        """
        Sets the list of referenced reports.

        Args:
            reports (list[int]): List of integers representing the ATel numbers of reports that this report references. 
        """
        if list_is_type(reports, int):
            self._referenced_reports = reports
        else:
            raise TypeError("Referenced reports must be a valid list of ints.")

    def add_referenced_report(self, atel_num:int):
        """
        Adds a report that is referenced by this report.

        Args:
            atel_num (int): The ATel number of the referenced report to add. 
        """
        self._referenced_reports.append(int(atel_num))

    def remove_referenced_report(self, atel_num:int):
        """
        Removes a report that is referenced by this report.

        Args:
            atel_num (int): The ATel number of the referenced report to remove.

        Raises:
            ValueError: If the given ATel number is not contained in the list.
        """
        try:
            self._referenced_reports.remove(atel_num)
        except ValueError:
            raise ValueError("The list does not contain a report with the given ATel Number.")

class ImportedReport(ReportResult):
    """
    An object representing a report imported from The Astronomer’s Telegram. Contains all the information required to be stored in the database.
    """

    def __init__(self, atel_num:int, title:str, authors:str, body:str, submission_date:datetime, referenced_reports:list[int]=[], observation_dates:list[datetime]=[], keywords:list[str]=[], objects:list[str]=[], coordinates:list[SkyCoord]=[], referenced_by:list[int]=[]):
        """
        Creates a ImportedReport object with the specified fields.

        Args:
            atel_num (int): The ATel number associated with the report.
            title (str): The title of the report.
            authors (str): A string representing the authors of the report.
            body (str): The body text of the report. Must be <= 4000 characters.
            submission_date (datetime): A datetime object representing the date and time the report was submitted to The Astronomer's Telegram.
            referenced_reports (list[int], optional): List of ATel numbers of reports referenced by this report.
            observation_dates (list[datetime], optional): List of observation dates of the reported event/s.
            keywords (list[str], optional): List of the fixed keywords associated with the report.
            objects (list[str], optional): List of main IDs of objects associated with the report.
            coordinates (list[SkyCoord], optional): List of coordinates extracted from the report.
            referenced_by (list[int], optional): List of ATel numbers representing reports that reference this report.
        """
        super().__init__(atel_num, title, authors, body, submission_date, referenced_reports)
        self.keywords = keywords
        self.referenced_by = referenced_by
        self.observation_dates = observation_dates
        self.keywords = keywords
        self.objects = objects
        self.coordinates = coordinates

    def __str__(self)->str:
        """
        Returns:
            str: A description of the report.
        """
        return f"{super().__str__()} Observation Date/s: {self.observation_dates}. Keywords: {self.keywords}. Objects: {self.objects}. Coords: {self.coordinates}. Referenced by: {self.referenced_by}"

    @property
    def referenced_by(self)->list[int]:
        """
        List of integers representing the ATel numbers of reports that this report references. 
        """
        return self._referenced_by.copy()

    @referenced_by.setter
    def referenced_by(self, reports:list[int]):
        """
        Sets the list of reports that reference this report.

        Args:
            reports (list[int]): List of integers representing the ATel numbers of reports that reference this report. 
        """
        if list_is_type(reports, int):
            self._referenced_by = reports
        else:
            raise TypeError("Referenced By must be a valid list of integers.")

    def add_referenced_by(self, atel_num:int):
        """
        Adds a report that references this report.

        Args:
            atel_num (int): The ATel number of the referenced report to add. 
        """
        self._referenced_by.append(int(atel_num))

    def remove_referenced_by(self, atel_num:int):
        """
        Removes a report that references this report.

        Args:
            atel_num (int): The ATel number of the report to remove.

        Raises:
            ValueError: If the given ATel number is not contained in the list.
        """
        try:
            self._referenced_by.remove(atel_num)
        except ValueError:
            raise ValueError("The list does not contain a report with the given ATel Number.")

    @property
    def observation_dates(self)->list[datetime]:
        """
        List of datetime objects representing observation dates of the reported event/s.
        """
        return self._observation_dates.copy()

    @observation_dates.setter
    def observation_dates(self, dates:list[datetime]):
        """
        Sets the list of observation dates.

        Args:
            dates (list[datetime]): List of datetime objects representing observation dates of the reported event/s.
        """
        if list_is_type(dates, datetime):
            self._observation_dates = dates
        else:
            raise TypeError("Observation dates must be a valid list of datetime objects.")

    @property
    def keywords(self)->list[str]:
        """
        List of strings representing the fixed keywords associated with the report.
        """
        return self._keywords.copy()

    @keywords.setter
    def keywords(self, keywords:list[str]):
        """
        Sets the list of fixed keywords.

        Args:
            keywords (list[str]): List of strings representing the fixed keywords associated with the report.
        """
        if list_is_type(keywords, str):
            self._keywords = keywords
        else:
            raise TypeError("Keywords must be a valid list of strings.")

    @property
    def objects(self)->list[str]:
        """
        List of strings representing main IDs of objects associated with the report.
        """
        return self._objects.copy()

    @objects.setter
    def objects(self, objects:list[str]):
        """
        Sets the list of referenced objects.

        Args:
            objects (list[str]): List of strings representing main IDs of objects associated with the report.
        """
        if list_is_type(objects, str):
            self._objects = objects
        else:
            raise TypeError("Objects must be a valid list of strings.")

    @property
    def coordinates(self)->list[SkyCoord]:
        """
        List of SkyCoord objects representing coordinates extracted from the report.
        """
        return self._coordinates.copy()

    @coordinates.setter
    def coordinates(self, coords:list[SkyCoord]):
        """
        Sets the list of referenced coordinates.

        Args:
            coords (list[SkyCoord]): List of SkyCoord objects representing coordinates extracted from the report.
        """
        if list_is_type(coords, SkyCoord):
            self._coordinates = coords
        else:
            raise TypeError(
                "Coordinates must be a valid list of SkyCoord objects.")
