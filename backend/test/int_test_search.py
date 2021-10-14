"""
Backend integration test for search requirements. (FR6, 7, 8, 10)

Author:
    Ryan Martin

License Terms and Copyright:
    Copyright (C) 2021 Ryan Martin

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


import mysql
from mysql.connector import errorcode
from mysql.connector.cursor import MySQLCursor

from datetime import datetime
import unittest as ut
from unittest import mock
from unittest.mock import MagicMock

from astropy.coordinates.sky_coordinate import SkyCoord

from app import app
from model.ds.report_types import ReportResult
from controller.importer.importer import ReportAlreadyExistsError 
from controller.importer import importer
from controller.search import search
import model.db.db_interface as db


class TestFR6(ut.TestCase):
    ''' Functional Requirement 6:
        Description: The software must allow the user to search for ATels by
        Object ID.
    '''
    def setUp(self):
        self.app = app.test_client() 

        # Pre-requisites: ATel #76, #79, #82 imported in db.
        self.test_data_A = {
            "term": "",
            "search_mode": "name",
            "search_data": "M31",
            "keywords": [], 
            "keyword_mode": "any",
            "start_date": "",
            "end_date": ""
        }

        # Pre-requisites: ATel #87, #90, #91 imported in db. 
        self.test_data_B = {
            "term": "",
            "search_mode": "name",
            "search_data": "XTE J1751-305",
            "keywords": [], 
            "keyword_mode": "any",
            "start_date": "",
            "end_date": ""
        }

        try:
            # A
            importer.import_report(76)
            importer.import_report(79)
            importer.import_report(82)
            # B 
            importer.import_report(87)
            importer.import_report(90)
            importer.import_report(91)
        except ReportAlreadyExistsError:
            pass 

    
    def test_search_data_A(self):
        response = self.app.post('/search', json=self.test_data_A)

        # Assert the response is valid. 
        self.assertEqual(response.json.get('flag'), 1)

        reports_list = response.json.get('report_list')
        self.assertTrue(len(reports_list) >= 3)

        # Check to see if the ATels appear in results. 
        atel_nums = [] 
        for r in reports_list:
            for (k, v) in r.items():
                if k == 'atel_num':
                    atel_nums.append(v) 

        # Depending on db, there may be more than these 
        # reports for the object, which is why this is being tested
        # manually. 
        self.assertIn(76, atel_nums)
        self.assertIn(79, atel_nums)
        self.assertIn(82, atel_nums)

    
    def test_search_data_B(self):
        response = self.app.post('/search', json=self.test_data_B) 

        # Assert the response is valid. 
        self.assertEqual(response.json.get('flag'), 1)

        reports_list = response.json.get('report_list')
        self.assertTrue(len(reports_list) >= 3)

        # Check to see if the ATels appear in results. 
        atel_nums = [] 
        for r in reports_list:
            for (k, v) in r.items():
                if k == 'atel_num':
                    atel_nums.append(v) 

        # Depending on db, there may be more than these 
        # reports for the object, which is why this is being tested
        # manually. 
        self.assertIn(87, atel_nums)
        self.assertIn(90, atel_nums)
        self.assertIn(91, atel_nums)


class TestFR7(ut.TestCase):
    ''' Functional Requirement 7:
        Description: The software must retrieve and store object aliases and coordinates from SIMBAD when 
        an unknown object ID is entered as a search term, or 60 days have elapsed since the last update 
        for the specified object. The software must also link all reports that reference the specified 
        object.
    '''
    def setUp(self):
        self.app = app.test_client()


    def test_object_update(self): 
        test_coords = SkyCoord(0.0, 0.0, frame='icrs', unit=('deg','deg'))

        # connect to database
        cn = db._connect()
        cur: MySQLCursor = cn.cursor()

        # setup query
        query = ("insert into Objects" 
                " (objectID, ra, declination, lastUpdated)" 
                " values (%s, %s, %s, %s)")

        data = ("DB_TEST_OBJECT", round(test_coords.ra.deg, 10), round(test_coords.dec.deg, 10), "2018-01-01")

        # execute query and handle errors
        try:
            cur.execute(query, data)
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                pass
            else:
                raise e
        finally:
            cn.commit()
            cur.close()
            cn.close()

        exists, prev_last_updated = db.object_exists('DB_TEST_OBJECT') 
        self.assertTrue(exists)
        self.assertEqual(prev_last_updated, datetime(2018, 1, 1))

        db.add_aliases('DB_TEST_OBJECT', ['TEST1', 'TEST2'])

        exists, last_updated = db.object_exists('DB_TEST_OBJECT')
        self.assertLessEqual((last_updated - datetime.today()).days, 0)
        self.assertNotEqual(prev_last_updated, last_updated)


    def tearDown(self):
        cn = db._connect()
        cur = cn.cursor()
        cur.execute("delete from Objects where objectID = \"DB_TEST_OBJECT\"")
        cur.close()
        cn.commit()
        cn.close()


class TestFR8(ut.TestCase):
    ''' Functional Requirement 8:
        Description: The software must allow the user to search for ATels by
        a coordinate range.
    '''
    def setUp(self):
        # Set up test client 
        self.app = app.test_client() 

        # Fetch all the coordinate entires in the database. 
        self.coords = [] 

        cn = db._connect()
        cur: MySQLCursor = cn.cursor()

        query = ("select ra, declination from Objects")

        cur.execute(query)

        results = cur.fetchall()[:25] # First 25 coordinate results
        if len(results) != 25:
            self.fail('Need at least 25 coordinates in the database for this test.')

        if results:
            for result in results:
                ra = result[0]
                dec = result[1]
                self.coords.append(SkyCoord(ra, dec, frame='icrs', unit=('deg', 'deg')))
        else:
            self.fail('The database has no coordinate entries. Import ATels before runnning the test.')

    def test_coordinate_search(self):
        for coord in self.coords:

            ra_str = "{}:{}:{}".format(int(coord.ra.hms.h), abs(int(coord.ra.hms.m)), abs(coord.ra.hms.s))
            dec_str = "{}:{}:{}".format(int(coord.dec.dms.d), abs(int(coord.dec.dms.m)), abs(coord.dec.dms.s))
            radius_str = "10.0" # Default radius

            test_data = {
                "term": "",
                "search_mode": "coords",
                "search_data": [ra_str, dec_str, radius_str],
                "keywords": [], 
                "keyword_mode": "any",
                "start_date": "",
                "end_date": ""
            }

            all_results = []

            response = self.app.post('/search', json=test_data)
            try:
                # Assert the coordinates were valid. 
                self.assertEqual(response.json.get('flag'), 1)
                all_results.append(r for r in response.json.get('report_list'))
            except AssertionError as e:
                raise AssertionError(str(e) + ' for coordinates ' + ra_str + ', ' + dec_str)

            self.assertIsNotNone(all_results)
            self.assertFalse(len(all_results) == 0)


class TestFR10(ut.TestCase):
    ''' Functional Requirement 10:
        Description: The software must allow the user to search for ATels with any combination of a free-text 
        string, keyword selection and object (either object ID or coordinates) within a single query.
    '''
