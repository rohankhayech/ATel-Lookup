"""
Test suite for the public web interface modules. 

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

test_manual_success = {
    "import_mode": "manual",
    "atel_num": 1234
}

test_manual_fail = {
    "import_mode": "manual"
}

test_manual_fail_invalid_atel = {
    "import_mode": "manual",
    "atel_num": -87
}

test_auto_with_atel_num = {
    "import_mode": "auto",
    "atel_num": -6326
}

test_bad_import_mode_name_fail = {
    "import_mode": "garbage",
    "atel_num": 17722
}

test_auto_success_no_atel_given = {
    "import_mode": "auto",
}

test_report_not_found_error = {
    "import_mode": "manual",
    "atel_num": 74632
}

test_report_already_exists_error = {
    "import_mode": "manual",
    "atel_num": 9999
}

test_search_basic = {
    "term": "supermassive",
    "search_mode": "name",
    "search_data": "Basinski",
    "keywords": ["radio", "optical"],
    "keyword_mode": "all",
    "start_date": "2021-01-22",
    "end_date": "2021-06-22"
}

test_search_basic_coords = {
    "term": "supermassive",
    "search_mode": "coords",
    "search_data": ["13h36m50s", "30d10m35s", 3.4],
    "keywords": ["radio"],
    "keyword_mode": "none",
    "start_date": "2005-03-15",
    "end_date": "2010-09-12"
}

test_search_bad_date = {
    "term": "supermassive",
    "search_mode": "name",
    "search_data": "Basinski",
    "keywords": ["radio", "optical"],
    "keyword_mode": "any",
    "start_date": "2025-09-06",
    "end_date": "2029-06-22"
}

test_search_bad_search_mode = {
    "term": "supermassive",
    "search_mode": "thing",
    "search_data": "Basinski",
    "keywords": ["radio", "optical"],
    "keyword_mode": "any",
    "start_date": "2007-09-06",
    "end_date": "2009-06-22"
}

test_search_dates_backwards = {
    "term": "supermassive",
    "search_mode": "name",
    "search_data": "Basinski",
    "keywords": ["radio", "optical"],
    "keyword_mode": "any",
    "start_date": "2007-01-22",
    "end_date": "2003-06-22"
}

test_search_bad_ra_value = {
    "term": "supermassive",
    "search_mode": "coords",
    "search_data": [124.51, -22.022, 3.4],
    "keywords": ["radio", "optical"],
    "keyword_mode": "any",
    "start_date": "2001-01-22",
    "end_date": "2003-06-22"
}

test_search_bad_keyword = {
    "term": "supermassive",
    "search_mode": "coords",
    "search_data": ["13h36m50s", "30d10m35s", 3.4],
    "keywords": ["radio", "big rock"],
    "keyword_mode": "any",
    "start_date": "2001-01-22",
    "end_date": "2003-06-22"
}

test_search_term_only = {
    "term": "supermassive",
    "search_mode": "name",
    "keywords": ["radio", "optical"],
    "keyword_mode": "all",
    "start_date": "2021-01-22",
    "end_date": "2021-06-22"
}

test_object_coords_only_name = {
    "search_mode": "name",
    "search_data": "Basinski"
}

test_object_coords_only_coords = {
    "search_mode": "coords",
    "search_data": [88.51, 300.022, 3.4]
}

test_search_no_keywords = {
    "term": "supermassive",
    "search_mode": "name",
    "search_data": "Basinski",
    "start_date": "2021-01-22",
    "end_date": "2021-06-22"
}


     
class TestWebInterfaceImports(ut.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_imports_manual_success(self):
        response = self.app.post('/import', json = test_manual_success)
        self.assertEqual(response.json.get("flag"), 1) 
        cn = db._connect()
        cur = cn.cursor()
        cur.execute("delete from Reports where atelNum = 1234")
        cur.close()
        cn.commit()
        cn.close()
        # should show a successful manual import (both import mode and atel num given correctly)

    

    def test_imports_manual_fail(self): 
        response = self.app.post('/import', json = test_manual_fail)
        self.assertEqual(response.json.get("flag"), 0)
        #should show a failure (no atel number in json object)

    def test_imports_manual_fail_invalid_atel(self): 
        response = self.app.post('/import', json = test_manual_fail_invalid_atel)
        self.assertEqual(response.json.get("flag"), 0)
        #should show a failure (atel number provided but is 0 or less (invalid))

    def test_auto_with_atel_num(self): 
        pass
        # response = self.app.post('/import', json = test_auto_with_atel_num) # currently not working 8pm 22/09/2021 - ValueError: Body must be <= 4000 characters.
        # self.assertEqual(response.json.get("flag"), 1) 
        # Should succeed as the atel number is not needed with the auto import

    def test_bad_import_mode_name_fail(self): 
        response = self.app.post('/import', json = test_bad_import_mode_name_fail)
        self.assertEqual(response.json.get("flag"), 0)
        #Should fail as the import mode name is not correct

    def test_auto_success_no_atel_given(self): 
        pass
        # response = self.app.post('/import', json = test_auto_success_no_atel_given) # currently not working 8pm 22/09/2021 - ValueError: Body must be <= 4000 characters.
        # self.assertEqual(response.json.get("flag"), 1) 
        # Should succeed as auto import mode does not need an atel number

    def test_report_not_found_error(self):
        response = self.app.post('/import', json = test_report_not_found_error)
        self.assertEqual(response.json.get("flag"), 0) 
        #giving the function a atel number that does not exist, should give back report not found exception, and set flag to 0

    def test_report_already_exists_error(self):
        response = self.app.post('/import', json = test_report_already_exists_error)
        response = self.app.post('/import', json = test_report_already_exists_error)
        self.assertEqual(response.json.get("flag"), 0) 
        cn = db._connect()
        cur = cn.cursor()
        cur.execute("delete from Reports where atelNum = 9999")
        cur.close()
        cn.commit()
        cn.close()
    




class TestWebInterfaceSearch(ut.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.filters = SearchFilters(term="term")
        self.sample_coords = SkyCoord("20 54 05.689", "+37 01 17.38", unit=('hourangle','deg'))
        self.dt_now = datetime.now()
        self.dt_almost = datetime.now() - timedelta(days=59)
        self.dt_exact = datetime.now() - timedelta(days=60)
        self.dt_old = datetime.now() - timedelta(days=200)
        self.sample_report = ReportResult(1000, "Title", "Authors", "Body", self.dt_old, [])

    def test_search_basic(self): 
        response = self.app.post('/search', json = test_search_basic)
        self.assertEqual(response.json.get("flag"), 1)
        self.assertEqual(response.json.get("report_list"), [])
        self.assertEqual(response.json.get("nodes_list"), [[], []])
        # Should succeed doing a name search

    def test_search_basic_coords(self):
        response = self.app.post('/search', json = test_search_basic_coords)
        self.assertEqual(response.json.get("flag"), 1)
        self.assertEqual(response.json.get("report_list"), [])
        self.assertEqual(response.json.get("nodes_list"), [[], []])
        # Should succeed doing a coords search

    def test_search_term_only(self):
        response = self.app.post('/search', json = test_search_term_only)
        self.assertEqual(response.json.get("flag"), 1)
        self.assertEqual(response.json.get("report_list"), [])
        self.assertEqual(response.json.get("nodes_list"), [[], []])

    def test_search_bad_date(self):
        response = self.app.post('/search', json = test_search_bad_date)
        self.assertEqual(response.json.get("flag"), 0)
        # Should fail if a date is in the future

    def test_search_bad_search_mode(self):
        response = self.app.post('/search', json = test_search_bad_search_mode)
        self.assertEqual(response.json.get("flag"), 0)
        # Should fail if the search mode given is not "name" or "coords"

    def test_search_dates_backwards(self):
        response = self.app.post('/search', json = test_search_dates_backwards)
        self.assertEqual(response.json.get("flag"), 0)
        # if end date is before start date or vice versa, test should fail
    
    def test_search_bad_ra_value(self):
        pass
        # response = self.app.post('/search', json = test_search_bad_ra_value) # Outdated test needs to updated
        # self.assertEqual(response.json.get("flag"), 0)
        # Latitude angle(s) must be within -90 deg <= angle <= 90 deg

    def test_search_bad_keyword(self):
        response = self.app.post('/search', json = test_search_bad_keyword)
        self.assertEqual(response.json.get("flag"), 0)
        # keyword given is not in the FIXED_KEYWORD list, should fail

    def test_object_coords_only_name(self):
        response = self.app.post('/search', json = test_object_coords_only_name)
        self.assertEqual(response.json.get("flag"), 1)

    def test_search_no_keywords(self):
        response = self.app.post('/search', json = test_search_no_keywords)
        self.assertEqual(response.json.get("flag"), 1)


    #Testing Mocking Tests - none of this is implemented/working yet
    # return_value=({
    #         "atel_num": 11876,
    #         "title": "title",
    #         "authors": "a",
    #         "body": "b",
    #         "submission_date": "2021-01-01 00: 00: 00",
    #         "referenced_reports": [1400, 1650]
    #     })

    # @patch('app.search.search_reports_by_name', side_effect = return_value)
    # def first_test(self):
    #     mock = app.search
    #     mock.search_reports_by_name = MagicMock(return_value=({
    #         "atel_num": 11876,
    #         "title": "title",
    #         "authors": "a",
    #         "body": "b",
    #         "submission_date": "2021-01-01 00: 00: 00",
    #         "referenced_reports": [1400, 1650]
    #     }))
    #     response = self.app.post('/search', json = test_search_basic)
       

# Run suite. 
if __name__ == '__main__':
    ut.main()