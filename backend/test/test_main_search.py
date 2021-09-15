""" Test suite for the search module (internal)

These functions are used to access the SIMBAD database, providing a way to
search by name (ID) or coordinates. Data is formatted appropriately. 

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


from controller.search.search import UPDATE_OBJECT_DAYS
from model.constants import DEFAULT_RADIUS
from model.ds.report_types import ReportResult
from astropy.coordinates import SkyCoord
from model.ds.search_filters import SearchFilters
from controller.search.query_simbad import QuerySimbadError
from datetime import datetime, timedelta
import unittest as ut 
from unittest.mock import MagicMock

from controller.search import query_simbad as qs
from controller.search import search


class TestCheckObjectUpdates(ut.TestCase):
    def setUp(self):
        # Current date.
        self.dt_now = datetime.now()
        # Almost 60 days.
        self.dt_almost = datetime.now() - timedelta(days=59)
        # Exactly 60 days (requires updating)
        self.dt_exact = datetime.now() - timedelta(days=60)
        # More than 60 days (20 days, requires updating). 
        self.dt_old = datetime.now() - timedelta(days=200)


    def test_up_to_date(self):
        '''
        Case 1: Object is up-to-date already (the datetime is either today's date 
        or almosy 60 days). See the setUp method for details. 
        '''
        mock = search
        mock.qs.get_aliases = MagicMock()
        mock.db.add_aliases = MagicMock()

        # dt_now and dt_almost are less than 60 days. 
        mock.check_object_updates("object", self.dt_now) 
        mock.qs.get_aliases.assert_not_called()
        mock.db.add_aliases.assert_not_called()
        mock.check_object_updates("object", self.dt_almost) 
        mock.qs.get_aliases.assert_not_called()
        mock.db.add_aliases.assert_not_called()


    def test_needs_update_no_network(self):
        '''
        Case 2: The date is >= 60 days and needs updating, but there is a network error
        preventing the SIMBAD query. 
        '''
        mock = search 

        mock.qs.get_aliases = MagicMock(side_effect=QuerySimbadError("Error")) 
        mock.db.add_aliases = MagicMock() 

        with self.assertRaises(QuerySimbadError):
            mock.check_object_updates("object", self.dt_old)
            mock.check_object_updates("object", self.dt_exact)
            mock.qs.get_aliases.assert_called_with("object")
            mock.db.add_aliases.assert_called_with("object", [])


    def test_needs_update(self):
        '''
        Case 3: The date is >= 60 days and needs updating. 
        '''
        mock = search 
        
        # Case 1: SIMBAD does not find any aliases for the object. 
        mock.db.add_aliases = MagicMock() 
        mock.qs.get_aliases = MagicMock(return_value=[])

        mock.check_object_updates("test1", self.dt_old)
        mock.db.add_aliases.assert_called_once_with("test1", [])
        mock.qs.get_aliases.assert_called_with("test1")

        # Case 2: SIMBAD query returns alias list 
        mock.db.add_aliases = MagicMock() 
        mock.qs.get_aliases = MagicMock(return_value=["alias1", "alias2", "alias3"])

        mock.check_object_updates("test2", self.dt_old)
        mock.db.add_aliases.assert_called_once_with("test2", ["alias1", "alias2", "alias3"])
        mock.qs.get_aliases.assert_called_with("test2")


class TestSearchByName(ut.TestCase):
    def setUp(self): 
        self.filters = SearchFilters(term="term")
        self.sample_coords = SkyCoord("20 54 05.689", "+37 01 17.38", unit=('hourangle','deg'))
        self.dt_now = datetime.now()
        self.dt_almost = datetime.now() - timedelta(days=59)
        self.dt_exact = datetime.now() - timedelta(days=60)
        self.dt_old = datetime.now() - timedelta(days=200)
        self.sample_report = ReportResult(1000, "Title", "Authors", "Body", self.dt_old, [])


    def test_invalid_object(self):
        '''
        Case 1: An object that does not exist in either database. 
        '''
        mock = search 
        mock.db.object_exists = MagicMock(return_value=(False, None))
        mock.check_object_updates = MagicMock() 
        mock.db.get_object_coords = MagicMock()
        mock.qs.query_simbad_by_name = MagicMock(return_value=None)
        mock.db.add_object = MagicMock()
        mock.db.find_reports_by_object = MagicMock(return_value=None)

        # Call the mocked function. 
        self.assertEqual(mock.search_reports_by_name(self.filters, None, "name"), [])

        mock.check_object_updates.assert_not_called()
        mock.db.get_object_coords.assert_not_called() 
        mock.qs.query_simbad_by_name.assert_called_with("name", True)
        mock.db.add_object.assert_not_called()


    def test_object_in_db(self):
        '''
        Case 2: An object that exists in the local database, does NOT
        require updating (last_updated=dt.now)
        '''
        mock = search 
        mock.db.object_exists = MagicMock(return_value=(True, self.dt_now))
        mock.qs.query_simbad_by_name = MagicMock()
        mock.db.add_object = MagicMock()
        mock.db.add_aliases = MagicMock()
        mock.qs.get_aliases = MagicMock()
        mock.db.get_object_coords = MagicMock(return_value=self.sample_coords)
        mock.db.find_reports_by_object = MagicMock(return_value=[self.sample_report])
        mock.db.find_reports_in_coord_range = MagicMock(return_value=None)

        result = mock.search_reports_by_name(self.filters, None, "name")

        mock.db.object_exists.assert_called_with("name")
        mock.qs.query_simbad_by_name.assert_not_called()
        mock.db.get_object_coords.assert_called_with("name")
        mock.db.find_reports_by_object.assert_called_with(self.filters, "name")
        mock.db.find_reports_in_coord_range.assert_called_with(self.filters, self.sample_coords, DEFAULT_RADIUS)
        mock.db.add_object.assert_not_called()
        mock.db.add_aliases.assert_not_called()
        mock.qs.get_aliases.assert_not_called()

        diff = datetime.today() - self.dt_now
        self.assertFalse(diff.days >= UPDATE_OBJECT_DAYS)

        self.assertIsNotNone(result)
        self.assertEqual(result, [self.sample_report])


    def test_object_in_db(self):
        '''
        Case 3: An object that exists in the local database, and DOES
        require updating (last_updated=dt_old)
        '''
        mock = search 
        mock.db.object_exists = MagicMock(return_value=(True, self.dt_old))
        mock.db.get_object_coords = MagicMock(return_value=self.sample_coords)
        mock.qs.query_simbad_by_name = MagicMock()
        mock.db.add_object = MagicMock()
        mock.db.add_aliases = MagicMock()
        mock.qs.get_aliases = MagicMock()
        mock.db.find_reports_by_object = MagicMock(return_value=[self.sample_report])
        mock.db.find_reports_in_coord_range = MagicMock(return_value=None)

        mock.search_reports_by_name(self.filters, None, "name")

        self.assertEqual(mock.db.object_exists("name"), (True, self.dt_old))

        mock.db.object_exists.assert_called_with("name")
        mock.qs.query_simbad_by_name.assert_not_called()
        mock.db.add_object.assert_not_called()

        mock.check_object_updates.assert_called_with("name", self.dt_old)


    def test_object_not_in_db(self):
        '''
        Case 4: An object that exists in the SIMBAD database, but not the local database.
        '''
        mock = search 
        mock.db.object_exists = MagicMock(return_value=(False, None))
        mock.check_object_updates = MagicMock() 
        mock.qs.query_simbad_by_name = MagicMock(return_value=("mainid", self.sample_coords, ["alias1", "alias2"])) 
        mock.db.add_object = MagicMock()
        mock.db.get_object_coords = MagicMock(return_value=self.sample_coords)
        mock.db.find_reports_by_object = MagicMock(return_value=[self.sample_report])
        mock.db.find_reports_in_coord_range = MagicMock(return_value=None)

        result = mock.search_reports_by_name(self.filters, None, "name")

        mock.db.object_exists.assert_called_with("name")
        mock.check_object_updates.assert_not_called()
        mock.db.get_object_coords.assert_not_called()
        mock.qs.query_simbad_by_name.assert_called_with("name", True)
        mock.db.add_object.assert_called_with("mainid", self.sample_coords, ["alias1", "alias2"])
        mock.db.find_reports_by_object.assert_called_with(self.filters, None, "name")
        mock.db.find_reports_in_coord_range.assert_called_with(self.filters, None, self.sample_coords, DEFAULT_RADIUS)

        self.assertIsNotNone(result)
        self.assertNotEqual(result, [])
        self.assertEqual(result, [self.sample_report])


    def test_only_searchfilters(self):
        mock = search 

        # Within the if-statement (should not be called)
        mock.db.object_exists = MagicMock()
        mock.check_object_updates = MagicMock() 
        mock.db.get_object_coords = MagicMock()
        mock.db.add_object = MagicMock() 

        # Outside the if-statement:
        mock.db.find_reports_by_object = MagicMock(return_value=None)
        mock.db.find_reports_in_coord_range = MagicMock()

        mock.search_reports_by_name(self.filters, None, None)

        for func in [mock.db.object_exists, 
            mock.check_object_updates, 
            mock.db.get_object_coords, 
            mock.db.add_object,
            mock.db.find_reports_in_coord_range
        ]:
            func.assert_not_called()
        
        mock.db.find_reports_by_object.assert_called_with(self.filters, None, None)

        
    def test_invalid_imports(self):
        with self.assertRaises(ValueError):
            search.search_reports_by_name(None, None, None)


if __name__ == '__main__':
    ut.main()