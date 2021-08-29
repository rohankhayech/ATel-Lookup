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


from controller.search.query_simbad import QuerySimbadError
from datetime import datetime, timedelta
import unittest as ut 
from unittest.mock import MagicMock

from controller.search import query_simbad as qs
from controller.search import search


def none_return():
    return None 


class TestCheckObjectUpdates(ut.TestCase):
    def setUp(self):
        self.dt_now = datetime.now()
        self.dt_almost = datetime.now() - timedelta(days=59)
        self.dt_exact = datetime.now() - timedelta(days=60)
        self.dt_old = datetime.now() - timedelta(days=200)


    def test_up_to_date(self):
        search_mock = search
        search_mock.qs.get_aliases = MagicMock()

        search_mock._check_object_updates("object", self.dt_now) 
        search_mock.qs.get_aliases.assert_not_called()
        search_mock._check_object_updates("object", self.dt_almost) 
        search_mock.qs.get_aliases.assert_not_called()


    def test_needs_update_no_network(self):
        search_mock = search 

        search_mock.qs.get_aliases = MagicMock(side_effect=QuerySimbadError("Error")) 

        with self.assertRaises(QuerySimbadError):
            search_mock._check_object_updates("object", self.dt_old)
            search_mock._check_object_updates("object", self.dt_exact)


    def test_needs_update(self):
        search_mock = search 
        
        search_mock.db.add_aliases = MagicMock() 

        # Case 1: SIMBAD does not find any aliases for the object. 
        search_mock.qs.get_aliases = MagicMock(return_value=[])
        search_mock._check_object_updates("test", self.dt_old)
        search_mock.db.add_aliases.assert_called_once_with("test", [])

        search_mock.db.add_aliases = MagicMock() 

        # Case 2: SIMBAD query returns alias list 
        search_mock.qs.get_aliases = MagicMock(return_value=["alias1", "alias2", "alias3"])
        search_mock._check_object_updates("test", self.dt_old)
        search_mock.db.add_aliases.assert_called_once_with("test", ["alias1", "alias2", "alias3"])


if __name__ == '__main__':
    ut.main()