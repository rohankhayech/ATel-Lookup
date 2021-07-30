from datetime import datetime
from typing import List
from astropy.coordinates import SkyCoord
class ReportResult:
    """
    An object representing a report returned from the local database as a result of a search query. Contains all the information needed for displaying the report as a search result and on both the timeline and network graphs.
    """

    def __init__(self, atel_num:int, title:str, authors:str, body:str, submission_date:datetime, referenced_reports:List[int]=[]):
        """
        Creates a ReportResult object with the specified fields.

        Args:
            atel_num (int): The ATel number associated with the report.
            title (str): The title of the report.
            authors (str): A string representing the authors of the report.
            body (str): The body text of the report. Must be <= 4000 characters.
            submission_date (datetime): A datetime object representing the date and time the report was submitted to The Astronomer's Telegram.
            referenced_reports (List[int], optional): List of ATel numbers of reports referenced by this report.
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
        return self.__atel_num

    @atel_num.setter
    def atel_num(self, atel_num:int):
        """Sets the report's ATel number.

        Args:
            atel_num (int): A positive integer representing the ATel number associated with the report.

        Raises:
            ValueError: When the given ATel number is not a valid positive integer.
        """
        if atel_num>0 and atel_num<999999:
            self.__atel_num = atel_num
        else:
            raise ValueError("ATel Number must be a valid positive integer.")

    @property
    def title(self)->str:
        """
        The title of the report.
        """
        return self.__title

    @title.setter
    def title(self, title:str):
        """
        Sets the title of the report.

        Args:
            title (str): The title of the report.
        """
        self.__title = title

    @property
    def authors(self)->str:
        """
        A string representing the authors of the report.
        """
        return self.__authors

    @authors.setter
    def authors(self, authors:str):
        """Sets the authors of the report.

        Args:
            authors (str): A string representing the authors of the report.
        """
        self.__authors = authors

    @property
    def body(self)->str:
        """
        The body text of the report.
        """
        return self.__body

    @body.setter
    def body(self, body:str):
        """
        Sets the body text of the report.

        Args:
            body (str): The body text of the report. Must be 4000 characters or less.

        Raises:
            ValueError: When the given body text exceeds 4000 characters.
        """
        if (len(body)<=4000):
            self.__body = body
        else:
            raise ValueError("Body must be <= 4000 characters.")

    @property
    def submission_date(self)->datetime:
        """
        A Datetime object representing the date and time that the report was submitted to The Astronomer's Telegram.
        """
        return self.__submission_date

    @submission_date.setter
    def submission_date(self, date:datetime):
        """
        Sets the submission date of the report.

        Args:
            date (datetime): A Datetime object representing the date and time that the report was submitted to The Astronomer's Telegram.
        """
        self.__submission_date = date

    @property
    def referenced_reports(self)->List[int]:
        """
        List of integers representing the ATel numbers of reports that this report references. 
        """
        return self._referenced_reports.copy()

    @referenced_reports.setter
    def referenced_reports(self, reports:List[int]):
        """
        Sets the list of referenced reports.

        Args:
            reports (List[int]): List of integers representing the ATel numbers of reports that this report references. 
        """
        self._referenced_reports = reports

    def add_referenced_report(self, atel_num:int):
        """
        Adds a report that is referenced by this report.

        Args:
            atel_num (int): The ATel number of the referenced report to add. 
        """
        self._referenced_reports.append(atel_num)

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

    def __init__(self, atel_num:int, title:str, authors:str, body:str, submission_date:datetime, referenced_reports:List[int]=[], observation_dates:List[datetime]=[], keywords:List[str]=[], objects:List[str]=[], coordinates:List[SkyCoord]=[], referenced_by:List[int]=[]):
        """
        Creates a ImportedReport object with the specified fields.

        Args:
            atel_num (int): The ATel number associated with the report.
            title (str): The title of the report.
            authors (str): A string representing the authors of the report.
            body (str): The body text of the report. Must be <= 4000 characters.
            submission_date (datetime): A datetime object representing the date and time the report was submitted to The Astronomer's Telegram.
            referenced_reports (List[int], optional): List of ATel numbers of reports referenced by this report.
            observation_dates (List[datetime], optional): List of observation dates of the reported event/s.
            keywords (List[str], optional): List of the fixed keywords associated with the report.
            objects (List[str], optional): List of main IDs of objects associated with the report.
            coordinates (List[SkyCoord], optional): List of coordinates extracted from the report.
            referenced_by (List[int], optional): List of ATel numbers representing reports that reference this report.
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
    def referenced_by(self)->List[int]:
        """
        List of integers representing the ATel numbers of reports that this report references. 
        """
        return self.__referenced_by.copy()

    @referenced_by.setter
    def referenced_by(self, reports:List[int]):
        """
        Sets the list of reports that reference this report.

        Args:
            reports (List[int]): List of integers representing the ATel numbers of reports that reference this report. 
        """
        self.__referenced_by = reports

    def add_referenced_by(self, atel_num:int):
        """
        Adds a report that references this report.

        Args:
            atel_num (int): The ATel number of the referenced report to add. 
        """
        self.__referenced_by.append(atel_num)

    def remove_referenced_by(self, atel_num:int):
        """
        Removes a report that references this report.

        Args:
            atel_num (int): The ATel number of the report to remove.

        Raises:
            ValueError: If the given ATel number is not contained in the list.
        """
        try:
            self.__referenced_by.remove(atel_num)
        except ValueError:
            raise ValueError("The list does not contain a report with the given ATel Number.")

    @property
    def observation_dates(self)->List[datetime]:
        """
        List of datetime objects representing observation dates of the reported event/s.
        """
        return self.__observation_dates.copy()

    @observation_dates.setter
    def observation_dates(self, dates:List[datetime]):
        """
        Sets the list of observation dates.

        Args:
            dates (List[datetime]): List of datetime objects representing observation dates of the reported event/s.
        """
        self.__observation_dates = dates

    @property
    def keywords(self)->List[str]:
        """
        List of strings representing the fixed keywords associated with the report.
        """
        return self.__keywords.copy()

    @keywords.setter
    def keywords(self, keywords:List[str]):
        """
        Sets the list of fixed keywords.

        Args:
            keywords (List[str]): List of strings representing the fixed keywords associated with the report.
        """
        self.__keywords = keywords

    @property
    def objects(self)->List[str]:
        """
        List of strings representing main IDs of objects associated with the report.
        """
        return self.__objects.copy()

    @objects.setter
    def objects(self, objects:List[str]):
        """
        Sets the list of referenced objects.

        Args:
            objects (List[str]): List of strings representing main IDs of objects associated with the report.
        """
        self.__objects = objects

    @property
    def coordinates(self)->List[SkyCoord]:
        """
        List of SkyCoord objects representing coordinates extracted from the report.
        """
        return self.__coordinates.copy()

    @objects.setter
    def coordinates(self, coords:List[SkyCoord]):
        """
        Sets the list of referenced coordinates.

        Args:
            coords (List[SkyCoord]): List of SkyCoord objects representing coordinates extracted from the report.
        """
        self.__coordinates = coords