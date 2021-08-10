"""
Test suite for the database helper module. 

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
from typing import Tuple
import unittest

from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import IntegrityError

from model import db_helper

class TestInitTables(unittest.TestCase):
    #Verify tables exist/were created on container init
    def testTables(self):
        _verifyTable(self,"AdminUsers")
        _verifyTable(self, "Reports")
        _verifyTable(self,"Metadata")

def _verifyTable(self, table_name):
    cn = db_helper._connect()
    cur:MySQLCursor = cn.cursor()

    cur.execute(f"show tables like '{table_name}'")

    result = cur.fetchone()

    cur.close()
    cn.close()

    self.assertTrue(result)

class TestAuth(unittest.TestCase):
    
    def testAddUser(self):
        db_helper.add_admin_user("test","hash")
        self.assertTrue(db_helper.user_exists("test"))
    
    def testDupeUser(self):
        db_helper.add_admin_user("test", "hash")
        with (self.assertRaises(db_helper.ExistingUserError)):
            db_helper.add_admin_user("test","hash")

    def testUserNotExists(self):
        self.assertFalse(db_helper.user_exists("test2"))

    def testGetPassword(self):
        db_helper.add_admin_user("test", "hash")
        self.assertEqual(db_helper.get_hashed_password("test"),"hash")
        with (self.assertRaises(db_helper.UserNotFoundError)):
            db_helper.get_hashed_password("test2")

    def testExceedsMax(self):
        with (self.assertRaises(ValueError)):
            db_helper.add_admin_user("a"*26,"hash")
        with (self.assertRaises(ValueError)):
            db_helper.add_admin_user("test","a"*256)
        with (self.assertRaises(ValueError)):
            db_helper.add_admin_user("","hash")
        with (self.assertRaises(ValueError)):
            db_helper.add_admin_user("test","")

    def tearDown(self):
        #remove test user
        cn = db_helper._connect()
        cur:MySQLCursor = cn.cursor()
        cur.execute("delete from AdminUsers where username = 'test'")
        cur.close()
        cn.commit()
        cn.close()

if __name__ == '__main__':
    unittest.main()
