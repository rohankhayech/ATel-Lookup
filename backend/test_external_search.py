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


from controller.search.query_simbad import QuerySimbadError
import unittest as ut
import numpy as np
from unittest import mock
import requests

from controller.search import query_simbad

from astropy.table import Table
from astropy.table.column import Column
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
        self.assertListEqual(lst, ["id1", "id2", "id3", "id4"])
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


    def test_invalid_table(self):
        self.assertEqual(query_simbad._get_names_from_table(Table()), [])


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


    def test_invalid_table(self):
        with self.assertRaises(ValueError):
            query_simbad._get_coords_from_table(Table())


    def test_none_table(self):
        with self.assertRaises(ValueError):
            query_simbad._get_coords_from_table(None)


# Mock the situations where a network error occurs. 
# See the reference below. 
# Reference: https://github.com/astropy/astroquery/blob/main/astroquery/simbad/core.py 


def mocked_no_network(*args, **kwargs):
    raise requests.exceptions.HTTPError("Mocked error message.")


def mocked_blacklist(*args, **kwargs):
    raise requests.exceptions.ConnectionError("Mocked error message.")


# Mock the situation where no object is found. 
def mocked_object_not_found(*args, **kwargs):
    return None


# Unit testing for query_simbad_by_name() 
class TestNameSearch(ut.TestCase):
    # Test network error (no connection, mocked). 
    @mock.patch('astroquery.simbad.Simbad._request', side_effect=mocked_no_network)
    def test_no_network(self, _):
        with self.assertRaises(QuerySimbadError):
            query_simbad.query_simbad_by_name("test")


    # Test server blacklist (mocked). 
    @mock.patch('astroquery.simbad.Simbad._request', side_effect=mocked_blacklist)
    def test_blacklist(self, _):
        with self.assertRaises(QuerySimbadError):
            query_simbad.query_simbad_by_name("test")


    # Test object that does not exist (mocked)
    @mock.patch('astroquery.simbad.Simbad.query_object', side_effect=mocked_object_not_found)
    def test_no_object_found(self, _):
        # This function is patched by the mocked method. 
        self.assertIsNone(query_simbad.query_simbad_by_name("invalid_object"))


    # Test valid data. 
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


# Unit testing for query_simbad_by_coords()
class TestCoordSearch(ut.TestCase):
    def setUp(self): 
        # Sample SkyCoord object for testing.
        # Derived from the Hardvard SIMBAD mirror.
        # Reference: http://simbad.cfa.harvard.edu/simbad/sim-fcoo 
        self.sample_coords = SkyCoord("20 54 05.689", "+37 01 17.38", unit=('hourangle','deg'))
        # 30.0 arcseconds. 
        self.sample_radius = 20.0


    # Test with real data. 
    def test_coord_search(self):
        # Test a valid coordinate. 
        # Test whether the result is not empty. 
        # As this is real-world data, it is subject to change. 
        result = query_simbad.query_simbad_by_coords(self.sample_coords, self.sample_radius)
        self.assertIsNotNone(result) 
        self.assertNotEqual(result, { })
        self.assertIsNotNone(result.items)
        self.assertIsNotNone(result.values)
        self.assertIsNotNone(result.keys)

        for name in result:
            self.assertFalse(len(name) == 0)

        for aliases in result.items():
            self.assertIsNotNone(aliases)


    # See line 155 onwards. These are the same mocked functions, but for
    # the coordinate search method. 
    @mock.patch('astroquery.simbad.Simbad._request', side_effect=mocked_no_network)
    def test_no_network(self, _):
        with self.assertRaises(QuerySimbadError):
            query_simbad.query_simbad_by_coords(self.sample_coords, self.sample_radius)


    @mock.patch('astroquery.simbad.Simbad._request', side_effect=mocked_blacklist)
    def test_blacklist(self, _):
        with self.assertRaises(QuerySimbadError):
            query_simbad.query_simbad_by_coords(self.sample_coords, self.sample_radius)


    @mock.patch('astroquery.simbad.Simbad.query_region', side_effect=mocked_object_not_found)
    def test_no_object_found(self, _):
        self.assertIsNone(query_simbad.query_simbad_by_coords(self.sample_coords, self.sample_radius))


    # A 'None' SkyCoord should raise an error. 
    def test_invalid_coords(self):
        with self.assertRaises(ValueError):
            query_simbad.query_simbad_by_coords(None) 
    

    # Test radius (float between 0.0 and 20.0 inclusive)
    def test_invalid_radius(self):
        # This should fail as the radius should be validated already. 
        with self.assertRaises(ValueError):
            query_simbad.query_simbad_by_coords(self.sample_coords, 90.0)
            query_simbad.query_simbad_by_coords(self.sample_coords, -0.1)
    

    def test_radius_bounds(self):
        try:
            # None of these should fail as the radius value is on the boundaries. 
            # Because 0.0 is an exact radius, an object may not be found (therefore
            # a UserWarning may appear)
            query_simbad.query_simbad_by_coords(self.sample_coords, 0.0)
            query_simbad.query_simbad_by_coords(self.sample_coords, 10.0)
            query_simbad.query_simbad_by_coords(self.sample_coords, 20.0)
        except ValueError as e:
            self.fail(f"Function raised ValueError for valid radius: ${str(e)}")


# Run suite. 
if __name__ == '__main__':
    ut.main()