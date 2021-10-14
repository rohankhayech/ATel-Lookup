"""
Test for authentication, including user accounts and protected endpoints.

Author:
    Greg Lahaye

Contributors:
    Rohan Khayech

License Terms and Copyright:
    Copyright (C) 2021 Greg Lahaye, Rohan Khayech

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
from model.db.db_interface import get_hashed_password
from model.db import db_init, db_interface
from controller.authentication import add_admin_user
from controller.authentication import add_admin_user
from app import app

import unittest

import mysql.connector
from mysql.connector.cursor import MySQLCursor

class TestFR1_NFR15(unittest.TestCase):
    """
    The software must authenticate a user as an administrator before offering any of the below admin portal functions.
    The system must be extendible to allow a maintainer to add new administrator accounts when required.
    """
    test_username = "test_username"
    test_password = "test_password"

    def test_add_admin_user(self):
        add_admin_user(self.test_username, self.test_password)
        self.assertTrue(db_interface.user_exists(self.test_username))

    def test_login(self):
        self.test_add_admin_user()

        with app.test_client() as client:
            response = client.post(
                "/authenticate",
                json={
                    "username": self.test_username,
                    "password": self.test_password,
                },
            )

            self.assertIsNotNone(response.json)

    def test_import_unauthorized(self):
        with app.test_client() as client:
            response = client.post("/import")

            self.assertEqual(response.json.get("msg"), "Missing Authorization Header")

    def test_import(self):
        self.test_add_admin_user()

        with app.test_client() as client:
            response = client.post(
                "/authenticate",
                json={
                    "username": self.test_username,
                    "password": self.test_password,
                },
            )

            token = response.json

            json = {"import_mode": "manual", "atel_num": 1}
            headers = {"Authorization": f"Bearer {token}"}
            response = client.post("/import", json=json, headers=headers)

            self.assertIsNotNone(response.json.get("flag"))

    def tearDown(self):
        connection = db_interface._connect()
        cursor: MySQLCursor = connection.cursor()
        cursor.execute(
            "DELETE FROM AdminUsers WHERE username = %s", (self.test_username,)
        )
        cursor.close()
        connection.commit()
        connection.close()

class TestNFR13(unittest.TestCase):
    """
    Must store admin credentials securly, ensuring passwords are stored as a hashed value.
    """

    def setUp(self):
        add_admin_user("test_user", "password")

    def test_password_hashed(self):
        # Ensure password stored in database is not in plain text.
        self.assertNotEqual(get_hashed_password("test_user"), "password")

    def tearDown(self):
        delete_user("test_user")

#helper functions
def delete_user(user):
    # connect to database
    cn = db_init._connect()
    cur = cn.cursor()

    # execute query and handle errors
    try:
        cur.execute("delete from AdminUsers where username = %s;", (user,))
    except mysql.connector.Error as e:
        raise e
    finally:
        cn.commit()
        cur.close()
        cn.close()

if __name__ == "__main__":
    unittest.main()
