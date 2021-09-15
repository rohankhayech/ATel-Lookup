"""
Testing for importer and parser functions as well as custom exceptions.

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

import os
import unittest

from model.ds.report_types import ImportedReport
from model.db.db_interface import ExistingReportError
from controller.importer.importer import *
from controller.importer.parser import *

from unittest import mock
from unittest.mock import call
from bs4 import BeautifulSoup
from datetime import datetime
from requests.exceptions import ConnectionError, HTTPError
from pyppeteer.errors import TimeoutError

# Importer functions
class TestImporterFunctions(unittest.TestCase):
    # Tests import_report function
    @mock.patch('controller.importer.importer.add_report')
    @mock.patch('controller.importer.importer.download_report')
    @mock.patch('controller.importer.importer.report_exists')
    def test_manual_import(self, mock_report_exists, mock_download_report, mock_add_report):
        mock_report_exists.return_value = False

        # Reads HTML string of ATel #1000
        f = open(os.path.join('test', 'res', 'atel1000.html'), 'r')
        html_string = f.read()
        f.close()
        mock_download_report.return_value = html_string

        # Checks that add_report is called with expected ImportedReport object
        import_report(1000)
        mock_add_report.assert_called_with(parse_report(1000, html_string))

        # Reads HTML string of ATel #10000
        f = open(os.path.join('test', 'res', 'atel10000.html'), 'r')
        html_string = f.read()
        f.close()
        mock_download_report.return_value = html_string

        # Checks that add_report is called with expected ImportedReport object
        import_report(10000)
        mock_add_report.assert_called_with(parse_report(10000, html_string))

    # Tests import_all_reports function
    @mock.patch('controller.importer.importer.set_next_atel_num')
    @mock.patch('controller.importer.importer.import_report')
    @mock.patch('controller.importer.importer.get_next_atel_num')
    def test_auto_import(self, mock_get_next_atel_num, mock_import_report, mock_set_next_atel_num):
        # Expected import_report function calls
        expected_calls = [call(1), call(2), call(3), call(4), call(5)]

        mock_get_next_atel_num.return_value = 1
        mock_import_report.side_effect = [None, None, ReportAlreadyExistsError, None, ReportNotFoundError]

        # Checks for expected import_report function calls and that set_next_atel_num is called with expected integer
        import_all_reports()
        mock_import_report.assert_has_calls(expected_calls)
        mock_set_next_atel_num.assert_called_with(5)

        # Checks that import_report was not called with the argument 6
        try:
            mock_import_report.assert_has_calls([call(6)], any_order=True)
            raise Exception('\'import_report\' was called with the argument \'6\'')
        except AssertionError:
            pass
        except Exception as err:
            raise AssertionError(f'{str(err)}')

        # Expected import_report function calls
        expected_calls = [call(6), call(7), call(8)]

        mock_get_next_atel_num.return_value = 6
        mock_import_report.side_effect = [None, None, ImportFailError]

        # Checks for expected import_report function calls and that set_next_atel_num is called with expected integer
        import_all_reports()
        mock_import_report.assert_has_calls(expected_calls)
        mock_set_next_atel_num.assert_called_with(8)

        # Checks that import_report was not called with the argument 9
        try:
            mock_import_report.assert_has_calls([call(9)], any_order=True)
            raise Exception('\'import_report\' was called with the argument \'9\'')
        except AssertionError:
            pass
        except Exception as err:
            raise AssertionError(f'{str(err)}')

    # Tests download_report function
    def test_html_download(self):
        # ATel report titles for comparison
        titles = ['QPOs in 4U 1626-67', 'GB971227', 'Improved Coordinates for GB971227']

        # Tests HTML downloader for 3 ATels by comparing title outputs
        for i in range(3):
            html = download_report(i + 1)
            soup = BeautifulSoup(html, 'html.parser')
            self.assertEqual(soup.find('h1', {'class': 'title'}).get_text(), titles[i])
        
        # Tests HTML downloader for non-existing ATel
        html_string = download_report(9999999999)
        self.assertIsNone(html_string, 'Detecting non-existing ATel has failed')

# Parser functions
class TestParserFunctions(unittest.TestCase):
    # Tests parse_report function
    @mock.patch('controller.importer.parser.extract_keywords')
    def test_html_parser(self, mock_extract_keywords):
        mock_extract_keywords.return_value = []

        # Parses HTML of ATel #1000
        f = open(os.path.join('test', 'res', 'atel1000.html'), 'r')
        imported_report = parse_report(1000, f.read())
        f.close()

        # Retrieves ATel #1000 body text
        f = open(os.path.join('test', 'res', 'atel1000_body.txt'), 'r')
        body = f.read()
        f.close()

        self.assertEqual(imported_report.atel_num, 1000)
        self.assertEqual(imported_report.title, 'INTEGRAL observations of GX339-4: preliminary spectral fit results')
        self.assertEqual(imported_report.authors, 'M. D. Caballero-Garcia (LAEFF/INTA), J. Miller (Univ. of Michigan), E. Kuulkers (ESA/ESAC), M. Diaz Trigo (ESA/ESAC), on behalf of a larger collaboration')
        self.assertEqual(imported_report.body, body)
        self.assertEqual(imported_report.submission_date, datetime(year=2007, month=2, day=11, hour=9, minute=48))

        self.assertCountEqual(imported_report.referenced_reports, [])
        self.assertCountEqual(imported_report.observation_dates, [])
        self.assertCountEqual(imported_report.keywords, [])
        self.assertCountEqual(imported_report.objects, [])
        self.assertCountEqual(imported_report.coordinates, [])
        self.assertCountEqual(imported_report.referenced_by, [])

        # Parses HTML of ATel #10000
        f = open(os.path.join('test', 'res', 'atel10000.html'), 'r')
        imported_report = parse_report(10000, f.read())
        f.close()

        # Retrieves ATel #10000 body text
        f = open(os.path.join('test', 'res', 'atel10000_body.txt'), 'r')
        body = f.read()
        f.close()

        self.assertEqual(imported_report.atel_num, 10000)
        self.assertEqual(imported_report.title, 'ASASSN-17bd: Discovery of A Probable Supernova in 2MASX J15591858+1336487')
        self.assertEqual(imported_report.authors, 'J. Brimacombe (Coral Towers Observatory), J. S. Brown, K. Z. Stanek, T. W.-S. Holoien, C. S. Kochanek, J. Shields, T. A. Thompson (Ohio State), B. J. Shappee (Hubble Fellow, Carnegie Observatories), J. L. Prieto (Diego Portales; MAS), D. Bersier (LJMU), Subo Dong, S. Bose, Ping Chen (KIAA-PKU), R. A. Koff (Antelope Hills Observatory), G. Masi (Virtual Telescope Project, Ceccano, Italy), R. S. Post (Post Astronomy), G. Stone (Sierra Remote Observatories)')
        self.assertEqual(imported_report.body, body)
        self.assertEqual(imported_report.submission_date, datetime(year=2017, month=1, day=25, hour=5, minute=0))
        
        self.assertCountEqual(imported_report.referenced_reports, [])
        self.assertCountEqual(imported_report.observation_dates, [])
        self.assertCountEqual(imported_report.keywords, [])
        self.assertCountEqual(imported_report.objects, [])
        self.assertCountEqual(imported_report.coordinates, [])
        self.assertCountEqual(imported_report.referenced_by, [])

    # Tests extract_dates function
    def test_dates_extractor(self):
        self.assertCountEqual(extract_dates('210-Jan-2011 22:10:15'), [])
        self.assertCountEqual(extract_dates('22/495/2011 and 2020-3-555'), [])
        self.assertCountEqual(extract_dates('10-Jan-2011 22:10:15 and 11-06-99 9:55:34'), ['10-jan-2011 22:10:15', '11-06-99 9:55:34'])
        self.assertCountEqual(extract_dates('22-01-2006 5:44 and 2003/6/9 23:44'), ['22-01-2006 5:44', '2003/6/9 23:44'])
        self.assertCountEqual(extract_dates('17/06/1975 and 88/10/8'), ['17/06/1975', '88/10/8'])
        self.assertCountEqual(extract_dates('12-Mar-1938 11:45 and 2005-5-29'), ['12-mar-1938 11:45', '2005-5-29'])
        self.assertCountEqual(extract_dates('8/16/95 and 8/09/2005 6:45:33'), ['8/16/95', '8/09/2005 6:45:33'])
        self.assertCountEqual(extract_dates('1/03/2011 19:45:04 and 1958-1-2 5:33:22'), ['1/03/2011 19:45:04', '1958-1-2 5:33:22'])
        self.assertCountEqual(extract_dates('7-12-99 8:49 and 2013/8/15'), ['7-12-99 8:49', '2013/8/15'])
        self.assertCountEqual(extract_dates('1990/6/20 11:45:45 and 17-05-1940 00:05:23'), ['1990/6/20 11:45:45', '17-05-1940 00:05:23'])
        self.assertCountEqual(extract_dates('83/06/30 4:58 and 2017-5-20 18:30'), ['83/06/30 4:58', '2017-5-20 18:30'])
        self.assertCountEqual(extract_dates('10-Dec-2020 and 7/11/2005 06:39'), ['10-dec-2020', '7/11/2005 06:39'])
        self.assertCountEqual(extract_dates('17-02-88 and 9-Jul-36'), ['17-02-88', '9-jul-36'])
        self.assertCountEqual(extract_dates('16/5/93 03:45 and 7/30/1950 8:02'), ['16/5/93 03:45', '7/30/1950 8:02'])
        self.assertCountEqual(extract_dates('06/17/2000 06:42:16 and 10/13/1973'), ['06/17/2000 06:42:16', '10/13/1973'])
        self.assertCountEqual(extract_dates('80/6/5 and 9-Apr-00 14:14:14'), ['80/6/5', '9-apr-00 14:14:14'])
        self.assertCountEqual(extract_dates('7.3.2011 05:23:59 and 10/3/75'), ['7.3.2011 05:23:59', '10/3/75'])
        self.assertCountEqual(extract_dates('30-09-1998 and 14.10.1938 6:02'), ['30-09-1998', '14.10.1938 6:02'])
        self.assertCountEqual(extract_dates('9-Oct-73 10:39 and 07/29/99 04:27'), ['9-oct-73 10:39', '07/29/99 04:27'])
        self.assertCountEqual(extract_dates('15.7.2018 and 03/17/65 17:40:39'), ['15.7.2018', '03/17/65 17:40:39'])

    # Tests parse_dates function
    def test_dates_parser(self):
        pass

    # Tests extract_keywords function
    def test_keywords_extractor(self):
        self.assertCountEqual(extract_keywords('This is a test'), [])
        self.assertCountEqual(extract_keywords('The planet, exoplanet, planet(minor) are astronomical terms'), ['planet', 'exoplanet', 'planet(minor)'])
        self.assertCountEqual(extract_keywords('The PlAnet, exoPlAnEt, plANet(MINoR) are astronomical terms'), ['planet', 'exoplanet', 'planet(minor)'])
        self.assertCountEqual(extract_keywords('far-infra-red and infra-red'), ['far-infra-red', 'infra-red'])
        self.assertCountEqual(extract_keywords('comment'), [])
        self.assertCountEqual(extract_keywords('> gev, gravitatiOnal waves, graVitatIonal lenSiNg and waves'), ['> gev', 'gravitational waves', 'gravitational lensing'])
        self.assertCountEqual(extract_keywords('nova, ASTEROID(binary) and supernova remnant'), ['nova', 'asteroid', 'asteroid(binary)', 'binary', 'supernova remnant'])
        self.assertCountEqual(extract_keywords('Steve, a comment, euhemerism and agn'), ['a comment', 'agn'])
        self.assertCountEqual(extract_keywords('   ExopLANet'), ['exoplanet'])
        self.assertCountEqual(extract_keywords('black hole   '), ['black hole'])

# Custom exceptions
class TestCustomExceptions(unittest.TestCase):
    # Tests that ReportAlreadyExistsError is being raised
    @mock.patch('controller.importer.importer.add_report')
    @mock.patch('controller.importer.importer.parse_report')
    @mock.patch('controller.importer.importer.download_report')
    @mock.patch('controller.importer.importer.report_exists')
    def test_report_already_exists_error(self, mock_report_exists, mock_download_report, mock_parse_report, mock_add_report):
        mock_report_exists.return_value = True
        with self.assertRaises(ReportAlreadyExistsError):
            import_report(1)

        mock_report_exists.return_value = False
        mock_download_report.return_value = 'Test'
        mock_parse_report.return_value = ImportedReport(1, 'Title', 'Authors', 'Body', datetime(1999, 1, 1))
        mock_add_report.side_effect = ExistingReportError
        with self.assertRaises(ReportAlreadyExistsError):
            import_report(1)

    # Tests that ReportNotFoundError is being raised
    @mock.patch('controller.importer.importer.download_report')
    @mock.patch('controller.importer.importer.report_exists')
    def test_report_not_found_error(self, mock_report_exists, mock_download_report):
        mock_report_exists.return_value = False
        mock_download_report.return_value = None
        with self.assertRaises(ReportNotFoundError):
            import_report(1)

    # Tests that ImportFailError is being raised
    @mock.patch('controller.importer.importer.download_report')
    @mock.patch('controller.importer.importer.report_exists')
    def test_import_fail_error(self, mock_report_exists, mock_download_report):
        mock_report_exists.return_value = False

        mock_download_report.side_effect = NetworkError
        with self.assertRaises(ImportFailError):
            import_report(1)

        mock_download_report.side_effect = DownloadFailError
        with self.assertRaises(ImportFailError):
            import_report(1)

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
    def test_download_fail_error(self, mock_render):
        mock_render.side_effect = TimeoutError
        with self.assertRaises(DownloadFailError):
            download_report(1)

if __name__ == "__main__":
    unittest.main()