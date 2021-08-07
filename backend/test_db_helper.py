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

from model import db_helper

class TestInitTables(unittest.TestCase):
    def testTables(self):
        db_helper.init_db()
        
        cn = db_helper._connect()
        cur:MySQLCursor = cn.cursor()

        cur.execute("show tables like 'AdminUsers'")

        result = cur.fetchone()

        cur.close()
        cn.close()

        self.assertTrue(result)

class TestAuth(unittest.TestCase):
    def testAddUser(self):
        db_helper.add_admin_user("test","hash")
        self.assertTrue(db_helper.user_exists("test"))
    
    def testDupeUser(self):
        db_helper.add_admin_user("test","")

    def testUserNotExists(self):
        self.assertFalse(db_helper.user_exists("test2"))

    def testGetPassword(self):
        self.assertEqual(db_helper.get_hashed_password("test"),"hash")
        with (self.assertRaises(db_helper.UserNotFoundError)):
            db_helper.get_hashed_password("test2")

    def cleanUp(self):
        cn = db_helper._connect()
        cur = cn.cursor()
        cur.execute("delete from AdminUsers where username = 'test'")
        cur.close()
        cn.close()

if __name__ == '__main__':
    unittest.main()