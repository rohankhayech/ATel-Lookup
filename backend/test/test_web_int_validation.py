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
from multiprocessing import Value
from astropy.coordinates import SkyCoord
from typing import Tuple
from view.web_interface import none_check
from view.web_interface import keyword_mode_check
from view.web_interface import keywords_check
from view.web_interface import valid_date_check
from view.web_interface import req_fields_check
from view.web_interface import search_mode_check
from view.web_interface import valid_radius
from view.web_interface import valid_dec
from view.web_interface import valid_ra
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
        try:
            test_string = "2020-01-01"
            parse_date_input(test_string)
            self.assertEqual(parse_date_input(test_string),datetime(2020,1,1))
        except ValueError:
            self.fail("PARSE DATE INPUT: test_correct_date failed")

    def test_wrong_date(self):
        test_string = "200003-45-45"
        self.assertRaises(ValueError, parse_date_input, test_string)
        test_string = "2003:10-10"
        self.assertRaises(ValueError, parse_date_input, test_string)
        test_string = "12-13"
        self.assertRaises(ValueError, parse_date_input, test_string)


class TestParseSearchCoords(ut.TestCase):
    def test_correct_skycoord(self):
        ra = "13:36:50"
        dec = "30:10:35"
        skycoord_func = parse_search_coords(ra,dec)
        skycoord = SkyCoord(ra, dec, frame="icrs", unit=("hourangle", "deg"))
        self.assertEqual(skycoord_func, skycoord)


class TestRightAscensionValidation(ut.TestCase):
    def test_no_coords(self):
        ra = ""
        self.assertRaises(ValueError, valid_ra, ra)
        ra = None
        self.assertRaises(ValueError, valid_ra, ra)
    
    def test_bad_format(self):
        ra = "10HOURS13m10"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "16:51mins"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "165130.999"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "10:52"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = ":14:20.054"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "17h10:54:"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "10::10.0"
        self.assertRaises(ValueError, valid_ra, ra)

    def test_out_of_range(self):
        ra = "-30:10:10"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "30:10:10"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "10:-45:10"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "10:60:10"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "10:10:-20.0"
        self.assertRaises(ValueError, valid_ra, ra)
        ra = "10:10:85.92"
        self.assertRaises(ValueError, valid_ra, ra)

    def test_correct_coords(self):
        try:
            ra = "10:10:10"
            valid_ra(ra)
            ra = "20:54:12.273"
            valid_ra(ra)
            ra = "-12:59:43.4343"
            valid_ra(ra)
        except ValueError:
            self.fail("RA: test_correct_coords failed")

class TestDeclinationValidation(ut.TestCase):
    def test_no_coords(self):
        dec = ""
        self.assertRaises(ValueError, valid_dec, dec)
        dec = None
        self.assertRaises(ValueError, valid_dec, dec)
    
    def test_bad_format(self):
        dec = "10DEGREES13m10"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "16:51mins"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "165130.999"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "10:52"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = ":14:20.054"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "17d10:54:"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "10::10.0"
        self.assertRaises(ValueError, valid_dec, dec)

    def test_out_of_range(self):
        dec = "-1000:10:10"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "170:10:10"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "10:-45:10"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "10:60:10"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "10:10:-20.0"
        self.assertRaises(ValueError, valid_dec, dec)
        dec = "10:10:85.92"
        self.assertRaises(ValueError, valid_dec, dec)

    def test_correct_coords(self):
        try:
            dec = "88:10:10"
            valid_dec(dec)
            dec = "20:54:12.273"
            valid_dec(dec)
            dec = "-65:59:43.4343"
            valid_dec(dec)
        except ValueError:
            self.fail("DEC: test_correct_coords failed")


class TestRadiusValidation(ut.TestCase):
    def test_no_radius_given_success(self):
        try:
            rad = ""
            valid_radius(rad)
            rad = None
            valid_radius(rad)
        except ValueError:
            self.fail("RADIUS: test_no_radius_given_success failed")

    def test_out_of_range(self):
        rad = 45.0
        self.assertRaises(ValueError, valid_radius, rad)
        rad = -12.65
        self.assertRaises(ValueError, valid_radius, rad)

    def test_correct_radius(self):
        try:
            rad = 12.053
            valid_radius(rad)
            rad = 0.4
            valid_radius(rad)
        except ValueError:
            self.fail("RADIUS: test_correct_radius failed")

class TestSearchModeCheck(ut.TestCase):
    def test_correct_mode(self):
        try:
            search_mode = "coords"
            search_mode_check(search_mode)
            search_mode = "name"
            search_mode_check(search_mode)
        except ValueError:
            self.fail("SEARCH MODE: test_correct_mode failed")

    def test_wrong_mode(self):
        search_mode = "c0rds!"
        self.assertRaises(ValueError, search_mode_check, search_mode)
        search_mode = "AAAAAAAA"
        self.assertRaises(ValueError, search_mode_check, search_mode)


class TestReqFieldsCheck(ut.TestCase):
    def test_not_enough_fields(self):
        search_data_in = None
        keywords_in = None
        keyword_mode_in = None
        term_in = None
        self.assertRaises(ValueError, req_fields_check, search_data_in, keywords_in, keyword_mode_in, term_in)

    def test_enough_fields(self):
        try:
            search_data_in = None
            keywords_in = None
            keyword_mode_in = None
            term_in = "supermassive"
            req_fields_check(search_data_in, keywords_in, keyword_mode_in, term_in)
        except ValueError:
            self.fail("REQ FIELDS: test_enough_fields failed")


class TestDateCheck(ut.TestCase):
    def test_successful_dates(self):
        try:
            start_date = None
            end_date = None
            valid_date_check(start_date, end_date)

            start_date = "2020-01-01"
            start_date_datetime = datetime.strptime(start_date,"%Y-%m-%d")
            end_date = "2021-01-01"
            end_date_datetime = datetime.strptime(end_date,"%Y-%m-%d")
            valid_date_check(start_date_datetime, end_date_datetime)

            start_date = "2010-07-23"
            start_date_datetime = datetime.strptime(start_date,"%Y-%m-%d")
            end_date = "2016-11-11"
            end_date_datetime = datetime.strptime(end_date,"%Y-%m-%d")
            valid_date_check(start_date_datetime, end_date_datetime)
        except ValueError:
            self.fail("DATE CHECK: test_successful_dates failed")

    def test_bad_dates(self):
        start_date = "2020-01-01"
        start_date_datetime = datetime.strptime(start_date,"%Y-%m-%d")
        end_date = "2001-01-01"
        end_date_datetime = datetime.strptime(end_date,"%Y-%m-%d")
        self.assertRaises(ValueError, valid_date_check, start_date_datetime, end_date_datetime)

        start_date = "2024-01-01"
        start_date_datetime = datetime.strptime(start_date,"%Y-%m-%d")
        end_date = "2025-01-01"
        end_date_datetime = datetime.strptime(end_date,"%Y-%m-%d")
        self.assertRaises(ValueError, valid_date_check, start_date_datetime, end_date_datetime)

        start_date = "2006-01-01"
        start_date_datetime = datetime.strptime(start_date,"%Y-%m-%d")
        end_date = "2023-01-01"
        end_date_datetime = datetime.strptime(end_date,"%Y-%m-%d")
        self.assertRaises(ValueError, valid_date_check, start_date_datetime, end_date_datetime)


class TestKeywordsCheck(ut.TestCase):
    def test_good_keywords(self):
        try:
            keywords = ["exoplanet", "radio"]
            keywords_check(keywords)
        except ValueError:
            self.fail("KEYWORDS CHECK: test_good_keywords failed")

    def test_bad_keywords(self):
        keywords = ["bigrock"]
        self.assertRaises(ValueError, keywords_check, keywords)
        keywords = ["thing", "huge rock"]
        self.assertRaises(ValueError, keywords_check, keywords)


class TestKeywordModeCheck(ut.TestCase):
    def test_good_mode(self):
        try:
            keyword_mode = "all"
            keyword_mode_check(keyword_mode)
        except ValueError:
            self.fail("KEYWORD MODE: test_good_mode failed")

    def test_bad_mode(self):
        keyword_mode = "BAD"
        self.assertRaises(ValueError, keyword_mode_check, keyword_mode)
        keyword_mode = "121212121"
        self.assertRaises(ValueError, keyword_mode_check, keyword_mode)


class TestNoneCheck(ut.TestCase):
    def test_successful_check(self):
        try:
            term_in = "a"
            search_mode_in = "name"
            search_data_in = ""
            keywords_in = [""]
            keyword_mode_in = ""
            start_date_in = ""
            end_date_in = ""
            none_check(term_in, search_mode_in, search_data_in, keywords_in, keyword_mode_in, start_date_in, end_date_in)
        except ValueError:
            self.fail("NONE CHECK SUCCESS - FAILED")

    def test_unsuccessful_check(self):
        term_in = "a"
        search_mode_in = "name"
        search_data_in = ""
        keywords_in = [""]
        keyword_mode_in = ""
        start_date_in = ""
        end_date_in = None
        self.assertRaises(ValueError, none_check, term_in, search_mode_in, search_data_in, keywords_in, keyword_mode_in, start_date_in, end_date_in)

        


# Run suite. 
if __name__ == '__main__':
    ut.main()

