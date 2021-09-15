""" Test suite for the search module (external)

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


import requests
import unittest as ut
import numpy as np
import random as r
from enum import Enum 
from unittest import mock

from controller.search import query_simbad
from controller.search.query_simbad import QuerySimbadError
from model.constants import DEFAULT_RADIUS

from astropy.table import Table
from astropy.table.column import Column
from astropy.coordinates.sky_coordinate import SkyCoord


class TableType(Enum):
    QUERY_OBJECT=1
    QUERY_REGION=2
    QUERY_OBJECT_IDS=3


def create_mock_table(type: TableType) -> tuple[Table, str, SkyCoord, list[str]]:
    '''
        Create a mock astropy Table data structure with random values. 
        Also creates a random SkyCoord and alias list. 
        Random names are integer strings for simplicity. 

        Returns:
            Table: the mock table
            str: randomly generated MAIN_ID
            SkyCoord: randomly generated SkyCoord object. 
            list[str]: randomly generated list of aliases. 
            list[str]: randomly generated list of object IDs (where a table returns multiple MAIN_IDs)
    '''
    random_id = str(r.randint(1000, 9999))
    random_aliases = [] 
    random_objects = []

    for _ in range(0, r.randint(1, 15)):
        random_aliases.append(str(r.randint(1000, 9999)))

    random_ra_str = f"{r.randint(-23, 23)} {r.randint(0, 59)} {float(r.randint(0, 59))}"
    random_dec_str = f"{r.randint(0, 20)} {r.randint(0, 59)} {float(r.randint(0, 59))}"

    random_skycoord = SkyCoord(
        random_ra_str, 
        random_dec_str, 
        frame='icrs', 
        unit=('hourangle','deg')
    )

    mock_table = Table() 

    if type == TableType.QUERY_OBJECT:
        # Mocking a table similar to Simbad.query_object()
        col_1 = Column(name="MAIN_ID", data=[random_id], dtype=np.object0)
        col_2 = Column(name="RA", data=[random_ra_str], dtype=np.str0)
        col_3 = Column(name="DEC", data=[random_dec_str], dtype=np.str0)

        for col in [col_1, col_2, col_3]:
            mock_table.add_column(col)
    elif type == TableType.QUERY_OBJECT_IDS:
        # Mock an alias table similar to Simbad.query_objectids() 
        bytestrings = [] 

        for name in random_aliases:
            bytestrings.append(bytes(name, encoding='UTF-8'))

        col_1 = Column(name="ID", data=bytestrings, dtype=np.bytes0)

        mock_table.add_column(col_1)
    elif type == TableType.QUERY_REGION:
        # Generate a new list of random objects.
        num_objects = r.randint(1, 15)
        for _ in range(num_objects):
            random_objects.append(str(r.randint(1000, 9999)))
        col_1 = Column(name="MAIN_ID", data=random_objects, dtype=np.object0)

        random_ra_list = [] 
        random_dec_list = []
        r_ra_split = random_ra_str.split(' ')
        r_dec_split = random_dec_str.split(' ')

        for _ in range(num_objects):
            new_random_ra = f"{r_ra_split[0]} {r_ra_split[1]} {min(59.0, float(r_ra_split[2]) + round(abs((0.5 - r.random()) * DEFAULT_RADIUS)))}"
            new_random_dec = f"{r_dec_split[0]} {r_dec_split[1]} {min(59.0, float(r_ra_split[2]) + round(abs((0.5 - r.random()) * DEFAULT_RADIUS)))}"
            random_ra_list.append(new_random_ra)
            random_dec_list.append(new_random_dec)

        col_2 = Column(name="RA", data=random_ra_list, dtype=np.str0)
        col_3 = Column(name="DEC", data=random_dec_list, dtype=np.str0)

        for col in [col_1, col_2, col_3]:
            mock_table.add_column(col)

    return mock_table, random_id, random_skycoord, random_aliases, random_objects


########################################
# Unit testing: get_names_from_table() #
########################################
class TestNameExtraction(ut.TestCase):
    def setUp(self):
        self.table_1_data = create_mock_table(TableType.QUERY_OBJECT)
        self.table_2_data = create_mock_table(TableType.QUERY_OBJECT_IDS)
        self.table_3_data = create_mock_table(TableType.QUERY_REGION)


    # Test the id table (table 1)
    def test_id_table(self):
        # Expecting one name to be extracted. 
        result = query_simbad._get_names_from_table(self.table_1_data[0])
        self.assertNotEqual(result, [])
        self.assertEqual(len(result), 1)
        # Name extracted should be main ID. 
        self.assertEqual(result[0], self.table_1_data[1])
        for value in result:
            self.assertIsInstance(value, str)


    def test_alias_table(self):
        result = query_simbad._get_names_from_table(self.table_2_data[0])
        self.assertNotEqual(result, [])
        self.assertListEqual(result, self.table_2_data[3])
        for value in result:
            self.assertIsInstance(value, str)


    # Test the region table (dtype is object)
    def test_region_table(self):
        result = query_simbad._get_names_from_table(self.table_3_data[0])
        self.assertNotEqual(result, [])
        self.assertListEqual(result, self.table_3_data[4])
        for value in result:
            self.assertIsInstance(value, str)


    def test_invalid_table(self):
        self.assertEqual(query_simbad._get_names_from_table(Table()), [])


    def test_none_table(self):
        with self.assertRaises(ValueError):
            query_simbad._get_names_from_table(None)


#########################################
# Unit testing: get_coords_from_table() #
#########################################
class TestCoordExtraction(ut.TestCase):
    def setUp(self):
        self.tables = []
        for _ in range(50):
            self.tables.append(create_mock_table(TableType.QUERY_REGION))
        

    def test_tables(self):
        for table in self.tables:
            result = query_simbad._get_coords_from_table(table[0])
            self.assertIsNotNone(result) 
            self.assertAlmostEqual(0.0, table[2].separation(result).radian, places=2)


    def test_invalid_table(self):
        with self.assertRaises(ValueError):
            query_simbad._get_coords_from_table(Table())


    def test_none_table(self):
        with self.assertRaises(ValueError):
            query_simbad._get_coords_from_table(None)


# Mock the situations where a network error occurs.
# Used by both query_...() functions.  
# See the reference below. 
# Reference: https://github.com/astropy/astroquery/blob/main/astroquery/simbad/core.py 
def mocked_no_network(*args, **kwargs):
    raise requests.exceptions.HTTPError("Mocked error message.")


def mocked_blacklist(*args, **kwargs):
    raise requests.exceptions.ConnectionError("Mocked error message.")


# Mock the situation where no object is found. 
def mocked_object_not_found(*args, **kwargs):
    return None


def mocked_object_table(*args, **kwargs):
    return create_mock_table(TableType.QUERY_OBJECT)[0]


def mocked_objectids_table(*args, **kwargs):
    return create_mock_table(TableType.QUERY_OBJECT_IDS)[0]


def mocked_region_table(*args, **kwargs):
    return create_mock_table(TableType.QUERY_REGION)[0]


########################################
# Unit testing: query_simbad_by_name() #
########################################
class TestNameSearch(ut.TestCase):
    # Test network error (no connection, mocked). 
    @mock.patch('controller.search.query_simbad.Simbad._request', new=mocked_no_network)
    def test_no_network(self):
        with self.assertRaises(QuerySimbadError):
            query_simbad.query_simbad_by_name("test")


    # Test server blacklist (mocked). 
    @mock.patch('controller.search.query_simbad.Simbad._request', new=mocked_blacklist)
    def test_blacklist(self):
        with self.assertRaises(QuerySimbadError):
            query_simbad.query_simbad_by_name("test")


    # Test object that does not exist (mocked)
    @mock.patch('controller.search.query_simbad.Simbad.query_object', new=mocked_object_not_found)
    def test_no_object_found(self):
        # This function is patched by the mocked method. 
        self.assertEqual(query_simbad.query_simbad_by_name("invalid_object"), [])


    # Test a standard object search.
    @mock.patch('controller.search.query_simbad.Simbad.query_object', new=mocked_object_table)
    @mock.patch('controller.search.query_simbad.Simbad.query_objectids', new=mocked_objectids_table)
    def test_query_object(self):
        main_id, coords, aliases = query_simbad.query_simbad_by_name('M  1', True)
        self.assertIsNotNone(main_id)
        self.assertIsNotNone(coords)
        self.assertIsNotNone(aliases)
        self.assertFalse(len(aliases) == 0)


##########################################
# Unit testing: query_simbad_by_coords() #
##########################################
class TestCoordSearch(ut.TestCase):
    def setUp(self): 
        # Sample SkyCoord object for testing.
        # Derived from the Hardvard SIMBAD mirror.
        # Reference: http://simbad.cfa.harvard.edu/simbad/sim-fcoo 
        self.sample_coords = SkyCoord("20 54 05.689", "+37 01 17.38", unit=('hourangle','deg'))
        # 20.0 arcseconds. 
        self.sample_radius = 20.0


    @mock.patch('controller.search.query_simbad.Simbad.query_region', new=mocked_region_table)
    @mock.patch('controller.search.query_simbad.Simbad.query_objectids', new=mocked_objectids_table)
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
    @mock.patch('controller.search.query_simbad.Simbad._request', new=mocked_no_network)
    def test_no_network(self):
        with self.assertRaises(QuerySimbadError):
            query_simbad.query_simbad_by_coords(self.sample_coords, self.sample_radius)


    @mock.patch('controller.search.query_simbad.Simbad._request', new=mocked_blacklist)
    def test_blacklist(self):
        with self.assertRaises(QuerySimbadError):
            query_simbad.query_simbad_by_coords(self.sample_coords, self.sample_radius)


    @mock.patch('controller.search.query_simbad.Simbad.query_region', new=mocked_object_not_found)
    def test_no_object_found(self):
        self.assertEqual(query_simbad.query_simbad_by_coords(self.sample_coords, self.sample_radius), [])


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
    

    @mock.patch('controller.search.query_simbad.Simbad.query_region', new=mocked_object_not_found)
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