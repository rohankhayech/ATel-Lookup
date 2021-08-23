""" Unit testing suite for the search module (internal)

These functions include mocking for other modules (i.e., the database 
module) to ensure the search components are tested in isolation. 

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


from datetime import datetime
import random as r
from enum import Enum
import unittest as ut
from unittest import mock

import numpy as np

from astropy.coordinates.sky_coordinate import SkyCoord
from astropy.table.table import Table 
from astropy.table.column import Column

from controller.search import search as search
from model.constants import DEFAULT_RADIUS


######################
# Mocking functions. #
######################


class TableType(Enum):
    QUERY_OBJECT=1
    QUERY_REGION=2
    QUERY_OBJECT_IDS=3


def none_return():
    return None 


def db_add_object_stub(object_id: str, coords: SkyCoord, aliases: list[str]):
    pass 


def db_mock_object_dne() -> tuple[bool, datetime]:
    return False, None 


def db_mock_object_exists() -> tuple[bool, datetime]:
    return True, datetime.today() 


# TODO: Move this to the other test suite for more robust and reliable testing.
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
    '''
    random_id = str(r.randint(1000, 9999))
    random_aliases = [] 

    for _ in range(0, r.randint(1, 15)):
        random_aliases.append(str(r.randint(1000, 9999)))

    random_ra_str = f"${float(r.randint(0, 20))} ${float(r.randint(0, 20))} ${float(r.randint(0, 20))}"
    random_dec_str = f"${float(r.randint(0, 20))} ${float(r.randint(0, 20))} ${float(r.randint(0, 20))}"

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
            bytestrings.append(bytes(name))

        col_1 = Column(name="ID", data=bytestrings, dtype=np.bytes0)

        mock_table.add_column(col_1)
    elif type == TableType.QUERY_REGION:
        # Generate a new list of random objects.
        num_objects = r.randint(1, 15)
        random_objects = []
        for _ in range(num_objects):
            random_objects.append(str(r.randint(1000, 9999)))
        col_1 = Column(name="MAIN_ID", data=random_objects, dtype=np.object0)

        random_ra_list = [] 
        random_dec_list = []
        r_ra_split = random_ra_str.split(' ')
        r_dec_split = random_dec_str.split(' ')

        for _ in range(num_objects):
            new_random_ra = f"${r_ra_split[0]} ${r_ra_split[1]} ${r_ra_split[2] + r.random(-DEFAULT_RADIUS/2, DEFAULT_RADIUS/2)}"
            new_random_dec = f"${r_dec_split[0]} ${r_dec_split[1]} ${r_dec_split[2] + r.random(-DEFAULT_RADIUS/2, DEFAULT_RADIUS/2)}"
            random_ra_list.append(new_random_ra)
            random_dec_list.append(new_random_dec)

        col_2 = Column(name="RA", data=random_ra_list, dtype=np.str0)
        col_3 = Column(name="DEC", data=random_dec_list, dtype=np.str0)

        for col in [col_1, col_2, col_3]:
            mock_table.add_column(col)

    return mock_table, random_id, random_skycoord, random_aliases


class TestSearchByName(ut.TestCase):
    def setUp(self):
        pass


    # Don't actually use the db. 
    @mock.patch('model.db_helper.add_object', side_effect=db_add_object_stub)
    def test_new_object(self):
        '''
            Test case 1: user searches an object identifier that is valid,
            and is NOT in the local database. 
        '''
        pass