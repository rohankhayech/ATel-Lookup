from typing import List
from enum import Enum
from datetime import datetime

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

    def __init__(self, term:str=None, keywords:List[str]=None, keyword_mode:KeywordMode=KeywordMode.ANY, start_date:datetime=None, end_date:datetime=None):
        """
        Creates a SearchFilters object with the given criteria. Either term or keywords must be not None for the object to be valid.

        Args:
            term (str, optional): String representing a free-text search term. Defaults to None.
            keywords (List[str], optional): List of strings representing fixed keywords. Defaults to None.
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
        return ""

    @property
    def term(self)->str:
        """
        A free-text search term.
        """
        return self.__term

    @term.setter
    def term(self, term:str):
        """
        Sets the free-text search term.

        Args:
            term (str): String representing a free-text search term. 
        """
        self.__term = term

    @property
    def keywords(self)->List[str]:
        """
        The mode to use for filtering on keywords.
        """
        return self.__keywords.copy()

    @keywords.setter
    def keywords(self, keywords:List[str]):
        """
        Sets the list of keywords to filter by.

        Args:
            keywords (List[str]): List of strings representing fixed keywords.
        """
        self.__keywords = keywords

    @property 
    def keyword_mode(self)->KeywordMode:
        """
        The mode to use for filtering on keywords.
        """
        return self.__keyword_mode

    @keyword_mode.setter
    def keyword_mode(self, mode:KeywordMode):
        """
        Sets the mode to use for filtering on keywords.

        Args:
            mode (KeywordMode): Enum (ANY=0, ALL=1, NONE=2) representing the mode to use.

        Raises:
            TypeError: If the keyword mode is not valid.
        """
        if KeywordMode.has_value(mode):
            self.__keyword_mode = mode
        else:
            raise TypeError("Keyword mode must be a valid value of the KeywordMode enum.")

    @property
    def start_date(self)->datetime:
        """
        The start of the date range to filter by.
        """
        return self.__start_date

    @start_date.setter
    def start_date(self, date:datetime):
        """
        Sets the start date to filter by.

        Args:
            date (datetime): The start of the date range to filter by.
        """
        self.__start_date = date

    @property
    def end_date(self)->datetime:
        """
        The end of the date range to filter by.
        """
        return self.__end_date

    @end_date.setter
    def end_date(self, date:datetime):
        """
        Sets the end date to filter by.

        Args:
            date (datetime): The end of the date range to filter by.
        """
        self.__end_date = date