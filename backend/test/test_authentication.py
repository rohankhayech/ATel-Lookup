"""
Testing for importer and parser functions as well as custom exceptions.

Author:
    Greg Lahaye

License Terms and Copyright:
    Copyright (C) 2021 Nathan Sutardi

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

import unittest

from mysql.connector.cursor import MySQLCursor
from controller.authentication import add_admin_user, login
from model.db import db_interface
from app import app


# Importer functions
class TestImporterFunctions(unittest.TestCase):
    test_username = "test_username"
    test_password = "test_password"

    # @mock.patch("controller.importer.importer.add_report")
    # def test_create_admin_account(self, mock_report_exists):
    #     mock_report_exists.return_value = False

    #     db.add_admin_user(self.test_username, self.test_password)
    #     self.assertTrue(db.user_exists(self.test_username))

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

    def tearDown(self):
        connection = db_interface._connect()
        cursor: MySQLCursor = connection.cursor()
        cursor.execute(
            "DELETE FROM AdminUsers WHERE username = %s", (self.test_username,)
        )
        cursor.close()
        connection.commit()
        connection.close()


if __name__ == "__main__":
    unittest.main()
