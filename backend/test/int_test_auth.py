"""
Backend integration test for authentication requirements.

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
from backend.model.db.db_interface import get_hashed_password, user_exists
from model.db import db_init, db_interface
from backend.controller.authentication import InvalidCredentialsError, add_admin_user
import unittest

import mysql.connector

import app

class TestFR1(unittest.TestCase):
    """
    Authenticate a user as an admin before offering admin portal functions.
    """
    def setUp(self):
        self.client = app.test_client()
        add_admin_user("test_user", "password")
    
    def test_admin_not_authenticated(self):
        """Stub: Need help on this test."""

    def test_admin_authenticated(self):
        """Stub: Need help on this test."""

    def test_login(self):
        response = self.client.post("/authenticate",json=login_json)
        self.assertIsNotNone(response.json)

    def invalid_login(self):
        response = self.client.post("/authenticate", json=incorrect_login_json)
        self.assertEqual(response.json, "Invalid credentials")
        self.assertEqual(response.status_code,401)

    def tearDown(self):
        delete_user("test_user")

class TestNFR13(unittest.TestCase):
    """
    Must store admin credentials securly, ensuring passwords are stored as a hashed value.
    """
    def setUp(self):
        add_admin_user("test_user", "password")

    def test_password_hashed(self):
        self.assertNotEqual(get_hashed_password("test_user"),"password") # Ensure password stored in database is not in plain text.

    def tearDown(self):
        delete_user("test_user")

class TestNFR15(unittest.TestCase):
    """
    Must be extendible to allow a maintainer to add new admin accounts when required.

    Will be changed to test using CLI when implemented.
    """
    
    def test_add_account(self):
        #Test add user
        add_admin_user("test_user","password")
        self.assertTrue(user_exists("test_user"))

        #Fail on duplicate user
        with self.assertRaises(InvalidCredentialsError):
            add_admin_user("test_user", "password")

        # Clean up user
        delete_user("test_user")


import_json = {
        "import_mode": "manual",
        "atel_num": 1
}

login_json = {
    "username": "test_user",
    "password": "password"
}

incorrect_login_json = {
    "username": "test_user",
    "password": "wordpass"
}

#helper functions
def delete_user(user):
    # connect to database
    cn = db_init._connect()
    cur = cn.cursor()

    # execute query and handle errors
    try:
        cur.execute("delete from AdminUsers where username = %s;",(user,))
    except mysql.connector.Error as e:
        raise e
    finally:
        cn.commit()
        cur.close()
        cn.close()
