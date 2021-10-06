""" Test suite for the web_interface.py file - Web interface unit tests

Author:
    Tully Slattery

License Terms and Copyright:
    Copyright (C) 2021 Tully Slattery

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
from typing import Tuple
from view.web_interface import parse_date_input, parse_search_coords
from model.ds.search_filters import KeywordMode
from enum import Enum
import re
from model.constants import FIXED_KEYWORDS

from model.ds.search_filters import SearchFilters
from model.ds.report_types import ReportResult
from model.ds.search_filters import KeywordMode
import json
import unittest as ut

import json
import jwt
from datetime import datetime
from flask import Flask, jsonify
from requests.models import requote_uri
from datetime import datetime, timedelta
from astropy.coordinates import SkyCoord
from unittest.mock import MagicMock, patch
from controller.search import search
from model.db import db_interface as db
from app import app

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    current_user,
    jwt_required,
)

import requests
from unittest import mock


class TestParseDateInput(ut.TestCase):
    def setUp(self):
        self.testValue = 1
        
    def test_correct_date(self):
        test_string = "2020-01-01"
        test_string_datetime = datetime.strptime(test_string,"%Y-%m-%d")
        temp_date_obj = parse_date_input(test_string)
        self.assertEqual(temp_date_obj, test_string_datetime)

    def test_wrong_date(self):
        test_string = "2020-01-01"
        test_string_bad = "1950-06-06"
        test_string_datetime = datetime.strptime(test_string_bad,"%Y-%m-%d")
        temp_date_obj = parse_date_input(test_string)
        self.assertNotEqual(temp_date_obj, test_string_datetime)


class TestParseSearchCoords(ut.TestCase):
    def test_correct_skycoord(self):
        ra = "13:36:50"
        dec = "30:10:35"
        skycoord_func = parse_search_coords(ra,dec)
        skycoord = SkyCoord(ra, dec, frame="icrs", unit=("hourangle", "deg"))
        self.assertEqual(skycoord_func, skycoord)

    def test_wrong_skycoord(self):
        ra = "13:36:50"
        dec = "30:10:35"
        ra_bad = "18:16:20"
        dec_bad = "10:19:11"
        skycoord_func = parse_search_coords(ra,dec)
        skycoord_bad = SkyCoord(ra_bad, dec_bad, frame="icrs", unit=("hourangle", "deg"))
        self.assertNotEqual(skycoord_func, skycoord_bad)






# Run suite. 
if __name__ == '__main__':
    ut.main()

