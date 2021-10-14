"""
Backend integration tests for arbitrary non-functional requirements such as speed and security.

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

from datetime import datetime, timedelta
import statistics as st
import unittest

from model.constants import FIXED_KEYWORDS
from app import app

class TestNFR5(unittest.TestCase):
    """
    The database must return a complete set of results containing all valid reports matching the search criteria within an optimal and consistent time after a search query has been made. The system must return results for broad queries with a large number of results within a maximum of 30 minutes after a search query has been made.
    """

    def setUp(self):
        self.app = app.test_client()

    def test_wide_query_speed(self):
        request = {
            "term": " ",
            "search_data": "",
            "search_mode": "name",
            "keywords": FIXED_KEYWORDS,
            "keyword_mode": "any",
            "start_date": "1995-01-01",
            "end_date": "2021-10-14"
        }


        response_time:datetime = []
        
        start_time = datetime.now()
        response = self.app.post('/search', json=request)
        end_time = datetime.now()

        response_time = end_time - start_time

        # Ensure search returned successfully
        self.assertEqual(response.json.get("flag"), 1)
        self.assertIsNotNone(response.json.get("report_list"))

        # Check search took less than 30 minutes.
        if response_time > timedelta(seconds=1800):
            self.fail("Search took longer than 30 minutes.")

class TestNFR14(unittest.TestCase):
    """
    The system must perform input sanitisation on every user input field, including search and login fields to prevent malicious input such as special characters that could be used in an SQL injection attack.
    """

    def setUp(self):
        self.app = app.test_client()

    def test_sql_injection_prevention(self):
        # These queries should return all results on a vulnerable database.
        term_injection = {
            "term": "\" or 1=1; --",
            "search_data": "",
            "search_mode": "name",
            "keywords": [],
            "keyword_mode": "any",
            "start_date": "",
            "end_date": ""
        }
        object_injection = {
            "term": "\" or 1=1; --",
            "search_data": "",
            "search_mode": "name",
            "keywords": [],
            "keyword_mode": "any",
            "start_date": "",
            "end_date": ""
        }

        response = self.app.post('/search', json=term_injection)
        self.assertEqual(response.json.get("flag"), 1)
        self.assertListEqual(response.json.get("report_list"),[])

        response = self.app.post('/search', json=object_injection)
        self.assertEqual(response.json.get("flag"), 1)
        self.assertListEqual(response.json.get("report_list"), [])

        # This query should login as admin on a vulnerable database.
        username_injection = {
            "username": "\" or 1=1; --",
            "password": ""
        }
        response = self.app.post('/authenticate', json=username_injection)
        self.assertEqual(response.json,"Invalid credentials")
    
