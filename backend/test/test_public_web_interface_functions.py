"""
Test suite for the public web interface modules. 

Author:
    Tully Slattery

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
import json
import unittest as ut

import json
import jwt
from datetime import datetime
from flask import Flask, jsonify
from requests.models import requote_uri

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
    "atel_num": 14126
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

test_search_basic = {
    "search_mode": "name",
    "search_data": "Steph Curry",
    "keywords": "Deep threes, Swish",
    "keyword_mode": "All",
    "start_date": "2021-01-22",
    "end_date": "2021-06-22"
}

test_search_basic_coords = {
    "search_mode": "coords",
    "search_data": [263.520, -22.022, 3.4],
    "keywords": "Air ball, bricks, throwing stones",
    "keyword_mode": "None",
    "start_date": "2005-03-15",
    "end_date": "2010-09-12"
}


# success_flag = {
#     "flag": 0
# }
     
class TestWebInterfaceImports(ut.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_imports_manual_success(self): 
        response = self.app.post('/import', json = test_manual_success)
        self.assertEqual(response.json.get("flag"), 1)
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
        response = self.app.post('/import', json = test_auto_with_atel_num)
        self.assertEqual(response.json.get("flag"), 1)
        #Should succeed as the atel number is not needed with the auto import

    def test_bad_import_mode_name_fail(self): 
        response = self.app.post('/import', json = test_bad_import_mode_name_fail)
        self.assertEqual(response.json.get("flag"), 0)
        #Should fail as the import mode name is not correct

    def test_auto_success_no_atel_given(self): 
        response = self.app.post('/import', json = test_auto_success_no_atel_given)
        self.assertEqual(response.json.get("flag"), 1)
        #Should succeed as auto import mode does not need an atel number

    

    def test_import_calls(self):
        response = self.app.post('/import', json = test_manual_success)
        self.assertEqual(response.json.get("flag"), 1)
        #Here and below is where i will test the import_report and import_all_reports function calls + exception handling



class TestWebInterfaceSearch(ut.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_search_basic(self): 
        response = self.app.post('/search', json = test_search_basic)
        self.assertEqual(response.json.get("flag"), 1)
        

# Run suite. 
if __name__ == '__main__':
    ut.main()