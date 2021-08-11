"""
Testing for importer functions and exceptions.

Author:
    Nathan Sutardi

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

from controller.importer.importer import *
from bs4 import BeautifulSoup
from unittest import mock
from requests.exceptions import ConnectionError, HTTPError
from pyppeteer.errors import TimeoutError

# Importer functions
class TestImporterFunctions(unittest.TestCase):
    # Tests download_report function
    def test_html_download(self):
        # ATel report titles for comparison
        titles = ['QPOs in 4U 1626-67', 'GB971227', 'Improved Coordinates for GB971227']

        # Tests HTML downloader for 3 ATels by comparing title outputs
        for i in range(3):
            html = download_report(i + 1)
            soup = BeautifulSoup(html, 'html.parser')
            self.assertEqual(soup.find('h1', {'class': 'title'}).get_text(), titles[i])

# Importer exceptions
class TestImporterExceptions(unittest.TestCase):
    # Tests that NetworkError is being raised
    @mock.patch('requests_html.HTMLSession.get')
    def test_network_error(self, mock_get):
        mock_get.side_effect = ConnectionError
        with self.assertRaises(NetworkError):
            download_report(1)
        
        mock_get.side_effect = HTTPError
        with self.assertRaises(NetworkError):
            download_report(1)
    
    # Tests that DownloadFailError is being raised
    @mock.patch('requests_html.HTML.render')
    def test_download_fail_error(self, mock_get):
        mock_get.side_effect = TimeoutError
        with self.assertRaises(DownloadFailError):
            download_report(1)
    
if __name__ == "__main__":
    unittest.main()