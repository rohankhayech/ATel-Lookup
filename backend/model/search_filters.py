"""
Contains the SearchFilters data structure, used to pass common search criteria throughout the application.

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

from typing import Union
from enum import Enum
from datetime import datetime

from helper.type_checking import list_is_type

class KeywordMode(Enum):
    """
    Enum representing the mode to use for filtering on keywords.
    """
    ANY = 0
    ALL = 1
    NONE = 2

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 

class SearchFilters:
    """
    An object used to pass common search criteria throughout the application.
    """

    def __init__(self, term:Union[str,None]=None, keywords:Union[list[str],None]=None, keyword_mode:KeywordMode=KeywordMode.ANY, start_date:Union[datetime,None]=None, end_date:Union[datetime,None]=None):
        """
        Creates a SearchFilters object with the given criteria. Either term or keywords must be not None for the object to be valid.

        Args:
            term (str, optional): String representing a free-text search term. Defaults to None.
            keywords (list[str], optional): List of strings representing fixed keywords. Defaults to None.
            keyword_mode (KeywordMode, optional): The mode to use for filtering on keywords (ANY, ALL or NONE). Defaults to KeywordMode.ANY.
            start_date (datetime, optional): Datetime object representing the start of the date range to filter by. Defaults to None.
            end_date (datetime, optional): Datetime object representing the start of the date range to filter by. Defaults to None.

        Raises:
            TypeError: When neither term or keywords is specified or the list of keywords is empty when type is not specified.

        """
        if term or keywords:
            self.term = term
            self.keywords = keywords
            self.keyword_mode = keyword_mode
            self.start_date = start_date
            self.end_date = end_date
        else:
            if keywords == []:
                raise TypeError("List of keywords must be non-empty if term is not specified.")
            else:
                raise TypeError("Either term or keywords must be specfied.")

    def __str__(self) -> str:
        """
        Returns:
            str: A string describing the search filters specified by this object.
        """
        return f"Free text: {self.term}, Keywords ({self.keyword_mode.name}): {self.keywords}, Submitted between {self.start_date} and {self.end_date}"

    @property
    def term(self)->str:
        """
        A free-text search term.
        """
        return self._term

    @term.setter
    def term(self, term:str):
        """
        Sets the free-text search term.

        Args:
            term (str): String representing a free-text search term. 
        """
        self._term = str(term)

    @property
    def keywords(self)->list[str]:
        """
        The mode to use for filtering on keywords.
        """
        return self._keywords.copy()

    @keywords.setter
    def keywords(self, keywords:list[str]):
        """
        Sets the list of keywords to filter by.

        Args:
            keywords (list[str]): List of strings representing fixed keywords.
        """
        if list_is_type(keywords, str, allow_empty=False, allow_none=True):
            self._keywords = keywords
        else:
            raise TypeError("Keywords must be a valid list of strings or None.")

    @property 
    def keyword_mode(self)->KeywordMode:
        """
        The mode to use for filtering on keywords.
        """
        return self._keyword_mode

    @keyword_mode.setter
    def keyword_mode(self, mode:KeywordMode):
        """
        Sets the mode to use for filtering on keywords.

        Args:
            mode (KeywordMode): Enum (ANY=0, ALL=1, NONE=2) representing the mode to use.

        Raises:
            TypeError: If the keyword mode is not valid.
        """
        try:
            if KeywordMode.has_value(mode.value):
                self._keyword_mode = mode
            else:
                raise TypeError("Keyword mode must be a valid value of the KeywordMode enum.")
        except AttributeError:
            raise TypeError("Keyword mode must be a valid value of the KeywordMode enum.")

    @property
    def start_date(self)->datetime:
        """
        The start of the date range to filter by.
        """
        return self._start_date

    @start_date.setter
    def start_date(self, date:datetime):
        """
        Sets the start date to filter by.

        Args:
            date (datetime): The start of the date range to filter by.
        """
        if date == None or type(date) == datetime:
            self._start_date = date
        else:
            raise TypeError("Start date must be a valid datetime object.")

    @property
    def end_date(self)->datetime:
        """
        The end of the date range to filter by.
        """
        return self._end_date

    @end_date.setter
    def end_date(self, date:datetime):
        """
        Sets the end date to filter by.

        Args:
            date (datetime): The end of the date range to filter by.
        """
        if date == None or type(date) == datetime:
            self._end_date = date
        else:
            raise TypeError("End date must be a valid datetime object.")