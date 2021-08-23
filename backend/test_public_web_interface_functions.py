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

from app import A
import app

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    current_user,
    jwt_required,
)

app = Flask(__name__)
jwt = JWTManager(app)

import requests
from unittest import mock

test_manual = {
    "import_mode": "manual",
    "atel_num": "14126"
}

# def mocked_requests_get(*args, **kwargs): #create fake json
#     class MockResponse:
#         def __init__(self, json_data, status_code):
#             self.json_data = json_data
#             self.status_code = status_code

#         def json(self):
#             return self.json_data
    
#     if args[0] == 'manual test':
#         return MockResponse({"import_mode": "manual"}, 200)
#     elif args[0] == 'auto test':
#         return MockResponse({"import_mode": "automatic"}, 200)

#     return MockResponse(None, 404)

def mocked_requests_get():
    return test_manual
        

class TestWebInterface(ut.TestCase):
    @mock.patch('requests.get', side_effect = mocked_requests_get)
    def test_imports_manual(self, mock_get): #actual test module
        # Assert requests.get calls
        a = A()
        json_data = a.imports()
        self.assertEqual(json_data, {"import_mode": "manual"})
        json_data = a.imports()
        self.assertEqual(json_data, {"import_mode": "automatic"})
        json_data = a.imports()
        self.assertIsNone(json_data)

        self.assertEqual(len(mock_get.call_args_list), 3)
        

# Run suite. 
if __name__ == '__main__':
    ut.main()