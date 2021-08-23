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
    "atel_num": "14126"
}

test_manual_fail = {
    "import_mode": "manual"
}

success_flag = {
    "success_flag": 0
}
     
class TestWebInterface(ut.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_imports_manual_success(self): #actual test module
        response = self.app.post('/import', json = test_manual_success)
        print(response.json)
        # should show a successful manual import (both import mode and atel num given correctly)

    def test_imports_manual_fail(self): #actual test module
        response = self.app.post('/import', json = test_manual_fail)
        print(response.json)
        #should show a failure (no atel number in json object)

        

# Run suite. 
if __name__ == '__main__':
    ut.main()