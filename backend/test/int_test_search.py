"""
Backend integration test for search requirements. (FR...)

Author:
    Ryan Martin

License Terms and Copyright:
    Copyright (C) 2021 Rohan Khayech, Tully Slattery, Nathan Sutardi

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


import unittest as ut

from app import app
from controller.importer.importer import ReportAlreadyExistsError 
from controller.importer import importer


class TestFR6(ut.TestCase):
    ''' Functional Requirement 6:
        Description: The software must allow the user to search for ATels by
        Object ID.
    '''
    def setUp(self):
        self.app = app.test_client() 

        # Pre-requisites: ATel #76, #79, #82 imported in db.
        self.test_data_A = {
            "search_mode": "name",
            "search_data": "M31",
        }

        # Pre-requisites: ATel #87, #90, #91 imported in db. 
        self.test_data_B = {
            "search_mode": "name",
            "search_data": "XTE J1751-305"
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


class TestFR7:
    ''' Functional Requirement 7:
        Description: The software must retrieve and store object aliases and coordinates from SIMBAD when 
        an unknown object ID is entered as a search term, or 60 days have elapsed since the last update 
        for the specified object. The software must also link all reports that reference the specified 
        object.
    '''
    pass #NYI


class TestFR8:
    ''' Functional Requirement 8:
        Description: The software must allow the user to search for ATels by
        a coordinate range.
    '''
    pass #NYI


class TestFR10:
    ''' Functional Requirement 10:
        Description: The software must allow the user to search for ATels with any combination of a free-text 
        string, keyword selection and object (either object ID or coordinates) within a single query.
    '''
    pass #Partially implemented.