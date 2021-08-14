""" Test suite for the search module.

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


import unittest as ut
import warnings
import numpy as np
import random
from unittest import mock
import requests

from controller.search import query_simbad
from controller.search.query_simbad import QuerySimbadError

from astropy.table import Table
from astropy.table.column import Column
from astropy.coordinates.angles import Angle
from astropy.coordinates.sky_coordinate import SkyCoord


""" Test the get_names_from_table(Table) function. To test the real-world
    process, this test will construct a manual Table data structure using
    the same data types returned by the SIMBAD query functions. 
"""
class TestNameExtraction(ut.TestCase):
    def setUp(self):
        # This way of storing strings mirrors how the astroquery query 
        # function works. The string is represented as bytes. 
        col_1 = Column(name="ID", data=[b"id1", b"id2", b"id3", b"id4"])
        self.alias_table = Table()
        self.alias_table.add_column(col_1)

        # For region queries, astropy returns a column of objects for the 
        # main ID. This is different to an alias search which is an array of bytes. 
        col_2 = Column(name="MAIN_ID", data=["id1", "id2", "id3", "id4"], dtype=np.object0)
        col_3 = Column(name="RA", data=["", "", "", ""], dtype=np.str0)
        self.region_table = Table()
        self.region_table.add_column(col_2)
        self.region_table.add_column(col_3)


    # Test the alias table (dtype is bytes30)
    def test_alias_table(self):
        lst = query_simbad._get_names_from_table(self.alias_table)
        self.assertEqual(lst[0], "id1")
        self.assertEqual(lst[1], "id2")
        self.assertEqual(lst[2], "id3")
        self.assertEqual(lst[3], "id4")


    # Test the region table (dtype is object)
    def test_region_table(self):
        lst = query_simbad._get_names_from_table(self.region_table)
        self.assertEqual(lst[0], "id1")
        self.assertEqual(lst[1], "id2")
        self.assertEqual(lst[2], "id3")
        self.assertEqual(lst[3], "id4")


""" Test the coordinate extraction function. Like the TestNameExtraction class, 
    a mock table is created to mimic the format used by astroquery. 
"""
class TestCoordExtraction(ut.TestCase):
    def setUp(self):
        table_columns = ("MAIN_ID", "RA", "DEC", "COO_WAVELENGTH", "COO_BIBCODE")
        table_dtypes = ("object", "str", "str", "str", "object")

        # Reference objects are m13 and m1 respectively. 
        # COO_WAVE_LENGTH and COO_BIBCODE are excluded for simplicity. 
        table_ids = ("M 13", "M 1")
        table_ra = ("16 41 41.634", "05 34 31.94")
        table_dec = ("+36 27 40.75", "+22 00 52.2") 
        self._table_1 = Table(names=table_columns, dtype=table_dtypes)
        self._table_1.add_row(vals=(table_ids[0], table_ra[0], table_dec[0], "", None))
        self._table_2 = Table(names=table_columns, dtype=table_dtypes)
        self._table_2.add_row(vals=(table_ids[1], table_ra[1], table_dec[1], "", None))

        self.expected_coords_1 = SkyCoord(table_ra[0], table_dec[0], frame='icrs', unit=('hourangle', 'deg'))
        self.expected_coords_2 = SkyCoord(table_ra[1], table_dec[1], frame='icrs', unit=('hourangle', 'deg'))
        

    def test_table_1(self):
        # Extract the coordinates from the Table data structure. 
        coords_1 = query_simbad._get_coords_from_table(self._table_1)
        self.assertEqual(coords_1.ra, self.expected_coords_1.ra)
        self.assertEqual(coords_1.dec, self.expected_coords_1.dec)


    def test_table_2(self):
        coords_2 = query_simbad._get_coords_from_table(self._table_2)
        self.assertEqual(coords_2.ra, self.expected_coords_2.ra)
        self.assertEqual(coords_2.dec, self.expected_coords_2.dec)


# Mock the situations where a network error occurs. 
# See the reference below. 
# Reference: https://github.com/astropy/astroquery/blob/main/astroquery/simbad/core.py 


def mocked_no_network(*args, **kwargs):
    raise requests.exceptions.HTTPError("Mocked error message.")


def mocked_blacklist(*args, **kwargs):
    raise requests.exceptions.ConnectionError("Mocked error message.")


# A table is returned as None when no object is found. 
def mocked_no_result(*args, **kwargs):
    return None 


class TestNameSearch(ut.TestCase):
    @mock.patch('astroquery.simbad.Simbad._request', side_effect=mocked_no_network)
    def test_no_network(self, mock_get):
        with self.assertRaises(QuerySimbadError): 
            query_simbad.query_simbad_by_name("test")


    @mock.patch('astroquery.simbad.Simbad._request', side_effect=mocked_blacklist)
    def test_blacklist(self, mock_get):
        with self.assertRaises(QuerySimbadError):
            query_simbad.query_simbad_by_name("test")


    @mock.patch('astroquery.simbad.Simbad.query_object', side_effect=mocked_no_result)
    def test_no_object_found(self, mock_get):
        self.assertIsNone(query_simbad.query_simbad_by_name("fake_object"))


    def test_query_object(self):
        """ This test uses a real-world object listed in the SIMBAD database. 
            While this is not the ideal way to conduct unit testing, it is 
            required in order to test real data and use cases. 
        """
        main_id, coords, aliases = query_simbad.query_simbad_by_name('M 1', get_aliases=True)
        self.assertIsNotNone(main_id)
        self.assertIsNotNone(coords)
        self.assertIsNotNone(aliases)
        self.assertIsNot(len(aliases), 0)
        self.assertEqual(main_id, "M   1")
        # This test assumes that no astronomical object is ever called 
        # "bogus_object_name", which is a reasonable assumption...
        with self.assertWarns(UserWarning):
            # Random object name to avoid caching. 
            query_simbad.query_simbad_by_name(f"{random.randrange(10000, 99999)}")


    def test_mass_query(self):
        """ Query a random object identifier 100 times in immediate succession. 
            The SIMBAD server may blacklist the host IP address when 'spamming' is
            suspected. 
        """
        warnings.simplefilter('ignore')
        try:
            for _ in range(0, 100):
                query_simbad.query_simbad_by_name(f"{random.randrange(10000, 99999)}")
        except QuerySimbadError as e:
            self.fail(f"Mass query failed due to error: {str(e)}")
        except Exception as e2:
            self.fail(f"An unexpected exception occurred due to a network failure: ${str(e2)}")


# Run suite. 
if __name__ == '__main__':
    ut.main()