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

from model.ds.alias_result import AliasResult
from model.ds.report_types import ImportedReport
from model.db.db_interface import ExistingReportError
from controller.importer.importer import *
from controller.importer.parser import *

from unittest.mock import call
from unittest import mock
from bs4 import BeautifulSoup
from datetime import datetime
from astropy.coordinates import SkyCoord
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
        # Expected function calls
        expected_import_report_calls = [call(1), call(2), call(3), call(4), call(5)]
        expected_set_next_atel_num_calls = [call(2), call(3), call(4), call(5)]

        mock_get_next_atel_num.return_value = 1
        mock_import_report.side_effect = [None, None, ReportAlreadyExistsError, None, ReportNotFoundError]

        # Checks for expected import_report and set_next_atel_num function calls
        import_all_reports()
        mock_import_report.assert_has_calls(expected_import_report_calls)
        mock_set_next_atel_num.assert_has_calls(expected_set_next_atel_num_calls)

        # Checks that import_report was not called with the argument 6
        try:
            mock_import_report.assert_has_calls([call(6)], any_order=True)
            raise Exception('\'import_report\' was called with the argument \'6\'')
        except AssertionError:
            pass
        except Exception as err:
            raise AssertionError(f'{str(err)}')

        # Expected function calls
        expected_import_report_calls = [call(6), call(7), call(8)]
        expected_set_next_atel_num_calls = [call(7), call(8)]

        mock_get_next_atel_num.return_value = 6
        mock_import_report.side_effect = [None, None, ImportFailError]

        # Checks for expected import_report and set_next_atel_num function calls
        import_all_reports()
        mock_import_report.assert_has_calls(expected_import_report_calls)
        mock_set_next_atel_num.assert_has_calls(expected_set_next_atel_num_calls)

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
    @mock.patch('controller.importer.parser.parse_coords')
    @mock.patch('controller.importer.parser.extract_coords')
    @mock.patch('controller.importer.parser.extract_known_aliases')
    @mock.patch('controller.importer.parser.extract_keywords')
    @mock.patch('controller.importer.parser.parse_dates')
    @mock.patch('controller.importer.parser.extract_dates')
    def test_html_parser(self, mock_extract_dates, mock_parse_dates, mock_extract_keywords, mock_extract_known_aliases, mock_extract_coords, mock_parse_coords):
        mock_extract_dates.return_value = []
        mock_parse_dates.return_value = []
        mock_extract_keywords.return_value = []
        mock_extract_known_aliases.return_value = []
        mock_extract_coords.return_value = []
        mock_parse_coords.return_value = []

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

        self.assertCountEqual(imported_report.referenced_reports, [980, 986])
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

        # Parses HTML of ATel #12000
        f = open(os.path.join('test', 'res', 'atel12000.html'), 'r')
        imported_report = parse_report(12000, f.read())
        f.close()

        # Retrieves ATel #12000 body text
        f = open(os.path.join('test', 'res', 'atel12000_body.txt'), 'r')
        body = f.read()
        f.close()

        self.assertEqual(imported_report.atel_num, 12000)
        self.assertEqual(imported_report.title, 'INTEGRAL detects a rebrightening of the accreting millisecond X-ray pulsar IGR J17591-2342')
        self.assertEqual(imported_report.authors, 'C. Sanchez-Fernandez (ESAC, ESA), C. Ferrigno, J. Chenevez, E. Kuulkers, R. Wijnands, A. Bazzano, P. Jonker, M. Del Santo, on behalf of the INTEGRAL Galactic bulge monitoring team')
        self.assertEqual(imported_report.body, body)
        self.assertEqual(imported_report.submission_date, datetime(year=2018, month=9, day=1, hour=11, minute=24))
        
        self.assertCountEqual(imported_report.referenced_reports, [11941, 11981, 11957])
        self.assertCountEqual(imported_report.observation_dates, [])
        self.assertCountEqual(imported_report.keywords, [])
        self.assertCountEqual(imported_report.objects, [])
        self.assertCountEqual(imported_report.coordinates, [])
        self.assertCountEqual(imported_report.referenced_by, [12004])

        # Parses HTML of ATel #14000
        f = open(os.path.join('test', 'res', 'atel14000.html'), 'r')
        imported_report = parse_report(14000, f.read())
        f.close()

        # Retrieves ATel #14000 body text
        f = open(os.path.join('test', 'res', 'atel14000_body.txt'), 'r')
        body = f.read()
        f.close()

        self.assertEqual(imported_report.atel_num, 14000)
        self.assertEqual(imported_report.title, 'Optical polarization of AT2019wey')
        self.assertEqual(imported_report.authors, 'F. Bouzelou(Univ. of Crete, Greece), S. Kiehlmann (IA FORTH & Univ. of Crete, Greece), L. Markopoulioti (Univ. of Crete, Greece)')
        self.assertEqual(imported_report.body, body)
        self.assertEqual(imported_report.submission_date, datetime(year=2020, month=9, day=8, hour=19, minute=5))
        
        self.assertCountEqual(imported_report.referenced_reports, [13571, 13576, 13932, 13921, 13948, 13957, 13976, 13984])
        self.assertCountEqual(imported_report.observation_dates, [])
        self.assertCountEqual(imported_report.keywords, [])
        self.assertCountEqual(imported_report.objects, [])
        self.assertCountEqual(imported_report.coordinates, [])
        self.assertCountEqual(imported_report.referenced_by, [14003, 14100, 14168])

    # Tests extract_coords function
    def test_coords_extractor(self):
        self.assertCountEqual(extract_coords('There is no coordinates'), [])
        self.assertCountEqual(extract_coords('RA: 1111, DEC: -180.2, RB: +17.5, DEC: -55.4 and aRA 33.5 DEC 65.0'), [])
        self.assertCountEqual(extract_coords('RA: 10.0, DEC: 20.0 and RA: 224, DEC: -25.8'), ['ra: 10.0, dec: 20.0', 'ra: 224, dec: -25.8'])
        self.assertCountEqual(extract_coords('RA 42.5, DEC -15 and RA +75.5, DEC +44.3'), ['ra 42.5, dec -15', 'ra +75.5, dec +44.3'])
        self.assertCountEqual(extract_coords('RA: +16 DEC: -33.56 and RA: 0.05 DEC: +85.3'), ['ra: +16 dec: -33.56', 'ra: 0.05 dec: +85.3'])
        self.assertCountEqual(extract_coords('RA +355.48 DEC 89.9 and RA +64 DEC 75'), ['ra +355.48 dec 89.9', 'ra +64 dec 75'])
        self.assertCountEqual(extract_coords('RA -1170.30 DEC -63 and RA 400 DEC 30.2'), ['ra -1170.30 dec -63', 'ra 400 dec 30.2'])
        self.assertCountEqual(extract_coords('RA -00230.4 DEC 45 and RA +399.45 DEC -10'), ['ra -00230.4 dec 45', 'ra +399.45 dec -10'])
        self.assertCountEqual(extract_coords('RA: +22h45m32.3s, DEC: -77d55m17s and RA: +17h30m20s, DEC: +63d30m15.5s'), ['ra: +22h45m32.3s, dec: -77d55m17s', 'ra: +17h30m20s, dec: +63d30m15.5s'])
        self.assertCountEqual(extract_coords('RA 13h26m59s, DEC +32d06m33.4s and RA 08h49m06.4s, DEC 066d017m59s'), ['ra 13h26m59s, dec +32d06m33.4s', 'ra 08h49m06.4s, dec 066d017m59s'])
        self.assertCountEqual(extract_coords('RA: -06h59m17.4s DEC: -84d49m55.4s and RA: -19h02m55s DEC: +32d49m10.88s'), ['ra: -06h59m17.4s dec: -84d49m55.4s', 'ra: -19h02m55s dec: +32d49m10.88s'])
        self.assertCountEqual(extract_coords('RA -20h17m17.4s DEC 53d53m17s and RA 13h17m9.3s DEC 88d37m44s'), ['ra -20h17m17.4s dec 53d53m17s', 'ra 13h17m9.3s dec 88d37m44s'])
        self.assertCountEqual(extract_coords('RA: +17:33:44.6, DEC: 16:55:43 and RA: +023:17:8, DEC: +07:55:17.6'), ['ra: +17:33:44.6, dec: 16:55:43', 'ra: +023:17:8, dec: +07:55:17.6'])
        self.assertCountEqual(extract_coords('RA -08:017:17, DEC -55:03:55 and RA 10:10:10.10, DEC 60:17:45'), ['ra -08:017:17, dec -55:03:55', 'ra 10:10:10.10, dec 60:17:45'])
        self.assertCountEqual(extract_coords('RA: -19:50:07 DEC: -18:16:13.4 and RA: -05:2:5.4 DEC: +39:45:48'), ['ra: -19:50:07 dec: -18:16:13.4', 'ra: -05:2:5.4 dec: +39:45:48'])
        self.assertCountEqual(extract_coords('RA +16:31:58.3, DEC 75:0053:33.2 and RA -17:29:54, DEC +14:56:0.4'), ['ra +16:31:58.3, dec 75:0053:33.2', 'ra -17:29:54, dec +14:56:0.4'])

    # Tests parse_coords function
    @mock.patch('controller.importer.parser.add_object')
    @mock.patch('controller.importer.parser.query_simbad_by_name')
    @mock.patch('controller.importer.parser.check_object_updates')
    @mock.patch('controller.importer.parser.object_exists')
    @mock.patch('controller.importer.parser.query_simbad_by_coords')
    def test_coords_parser(self, mock_query_simbad_by_coords, mock_object_exists, mock_check_object_updates, mock_query_simbad_by_name, mock_add_object):
        mock_query_simbad_by_coords.return_value = dict()

        # Tests without querying SIMBAD
        self.assertCountEqual(parse_coords([]), [])
        self.assertCountEqual(parse_coords(['No coordinates', 'ra: 15:33:44, dec: 95:42:16']), [])
        self.assertCountEqual(parse_coords(['ra: 10.0, dec: 20.0', 'ra: 224, dec: -25.8']), [SkyCoord(10.0, 20.0, unit=('deg', 'deg')), SkyCoord(224.0, -25.8, unit=('deg', 'deg'))])
        self.assertCountEqual(parse_coords(['ra 42.5, dec -15', 'ra +75.5, dec +44.3']), [SkyCoord(42.5, -15.0, unit=('deg', 'deg')), SkyCoord(75.5, 44.3, unit=('deg', 'deg'))])
        self.assertCountEqual(parse_coords(['ra: +16 dec: -33.56', 'ra: 0.05 dec: +85.3']), [SkyCoord(16.0, -33.56, unit=('deg', 'deg')), SkyCoord(0.05, 85.3, unit=('deg', 'deg'))])
        self.assertCountEqual(parse_coords(['ra +355.48 dec 89.9', 'ra +64 dec 75']), [SkyCoord(355.48, 89.9, unit=('deg', 'deg')), SkyCoord(64.0, 75.0, unit=('deg', 'deg'))])
        self.assertCountEqual(parse_coords(['ra -1170.30 dec -63', 'ra 400 dec 30.2']), [SkyCoord(-1170.3, -63.0, unit=('deg', 'deg')), SkyCoord(400.0, 30.2, unit=('deg', 'deg'))])
        self.assertCountEqual(parse_coords(['ra -00230.4 dec 45', 'ra +399.45 dec -10']), [SkyCoord(-230.4, 45.0, unit=('deg', 'deg')), SkyCoord(399.45, -10.0, unit=('deg', 'deg'))])
        self.assertCountEqual(parse_coords(['ra: +22h45m32.3s, dec: -77d55m17s', 'ra: +17h30m20s, dec: +63d30m15.5s']), [SkyCoord('+22h45m32.3s', '-77d55m17s', unit=('hourangle', 'deg')), SkyCoord('+17h30m20s', '+63d30m15.5s', unit=('hourangle', 'deg'))])
        self.assertCountEqual(parse_coords(['ra 13h26m59s, dec +32d06m33.4s', 'ra 08h49m06.4s, dec 066d017m59s']), [SkyCoord('13h26m59s', '+32d06m33.4s', unit=('hourangle', 'deg')), SkyCoord('08h49m06.4s', '066d017m59s', unit=('hourangle', 'deg'))])
        self.assertCountEqual(parse_coords(['ra: -06h59m17.4s dec: -84d49m55.4s', 'ra: -19h02m55s dec: +32d49m10.88s']), [SkyCoord('-06h59m17.4s', '-84d49m55.4s', unit=('hourangle', 'deg')), SkyCoord('-19h02m55s', '+32d49m10.88s', unit=('hourangle', 'deg'))])
        self.assertCountEqual(parse_coords(['ra -20h17m17.4s dec 53d53m17s', 'ra 13h17m9.3s dec 88d37m44s']), [SkyCoord('-20h17m17.4s', '53d53m17s', unit=('hourangle', 'deg')), SkyCoord('13h17m9.3s', '88d37m44s', unit=('hourangle', 'deg'))])
        self.assertCountEqual(parse_coords(['ra: +17:33:44.6, dec: 16:55:43', 'ra: +023:17:8, dec: +07:55:17.6']), [SkyCoord('+17:33:44.6', '16:55:43', unit=('hourangle', 'deg')), SkyCoord('+023:17:8', '+07:55:17.6', unit=('hourangle', 'deg'))])
        self.assertCountEqual(parse_coords(['ra -08:017:17, dec -55:03:55', 'ra 10:10:10.10, dec 60:17:45']), [SkyCoord('-08:017:17', '-55:03:55', unit=('hourangle', 'deg')), SkyCoord('10:10:10.10', '60:17:45', unit=('hourangle', 'deg'))])
        self.assertCountEqual(parse_coords(['ra: -19:50:07 dec: -18:16:13.4', 'ra: -05:2:5.4 dec: 39:45:48']), [SkyCoord('-19:50:07', '-18:16:13.4', unit=('hourangle', 'deg')), SkyCoord('-05:2:5.4', '39:45:48', unit=('hourangle', 'deg'))])
        self.assertCountEqual(parse_coords(['ra +16:31:58.3, dec 75:0053:33.2', 'ra -17:29:54, dec +14:56:0.4']), [SkyCoord('+16:31:58.3', '75:0053:33.2', unit=('hourangle', 'deg')), SkyCoord('-17:29:54', '+14:56:0.4', unit=('hourangle', 'deg'))])

        expected_query_simbad_by_coords_calls = [call(SkyCoord(50.0, 60.0, unit=('deg', 'deg'))),
                                                 call(SkyCoord(120.0, 30.0, unit=('deg', 'deg')))
        ]

        expected_object_exists_calls = [call('main object 1'), call('main object 2'), call('main object 3'), call('main object 4')]
        
        expected_check_object_updates_calls = [call('main object 1', datetime(1999, 1, 1)),
                                               call('main object 2', datetime(1999, 1, 1)),
                                               call('main object 4', datetime(1999, 1, 1))
        ]

        expected_query_simbad_by_name_call = [call('main object 3', False)]
        expected_add_object_call = [call('main object 3', SkyCoord(10.0, 10.0, unit=('deg', 'deg')), ['alias 5', 'alias 6'])]
        
        mock_query_simbad_by_coords.side_effect = [dict([('main object 1', ['alias 1', 'alias 2']), ('main object 2', ['alias 3', 'alias 4'])]),
                                                   dict([('main object 3', ['alias 5', 'alias 6']), ('main object 4', ['alias 7', 'alias 8'])])
        ]

        mock_object_exists.side_effect = [(True, datetime(1999, 1, 1)), (True, datetime(1999, 1, 1)), (False, None), (True, datetime(1999, 1, 1))]
        mock_query_simbad_by_name.side_effect = [('main object 3', SkyCoord(10.0, 10.0, unit=('deg', 'deg')), [])]

        # Tests with querying SIMBAD
        self.assertCountEqual(parse_coords(['ra: 50.0, dec: 60.0', 'ra: 120.0, dec: 30.0']), [SkyCoord(50.0, 60.0, unit=('deg', 'deg')), SkyCoord(120.0, 30.0, unit=('deg', 'deg'))])
        mock_query_simbad_by_coords.assert_has_calls(expected_query_simbad_by_coords_calls)
        mock_object_exists.assert_has_calls(expected_object_exists_calls)
        mock_check_object_updates.assert_has_calls(expected_check_object_updates_calls)
        mock_query_simbad_by_name.assert_has_calls(expected_query_simbad_by_name_call)
        mock_add_object.assert_has_calls(expected_add_object_call)

    # Tests extract_dates function
    def test_dates_extractor(self):
        self.assertCountEqual(extract_dates('210-Jan-2011 22:10:15'), [])
        self.assertCountEqual(extract_dates('22/495/2011 and 2020-3-555'), [])
        self.assertCountEqual(extract_dates('10-Jan-2011; 22:10:15 and 11-06-99 9:55:34'), ['10-jan-2011; 22:10:15', '11-06-99 9:55:34'])
        self.assertCountEqual(extract_dates('22-01-2006 5:44 and 2003/6/9; 23:44'), ['22-01-2006 5:44', '2003/6/9; 23:44'])
        self.assertCountEqual(extract_dates('17/06/1975 and 88/10/8'), ['17/06/1975', '88/10/8'])
        self.assertCountEqual(extract_dates('12-Mar-1938 11:45 and 2005-5-29'), ['12-mar-1938 11:45', '2005-5-29'])
        self.assertCountEqual(extract_dates('8/16/95 and 8/09/2005 6:45:33'), ['8/16/95', '8/09/2005 6:45:33'])
        self.assertCountEqual(extract_dates('1/03/2011 19:45:04 and 1958-1-2; 5:33:22'), ['1/03/2011 19:45:04', '1958-1-2; 5:33:22'])
        self.assertCountEqual(extract_dates('7-12-99; 8:49 and 2013/8/15'), ['7-12-99; 8:49', '2013/8/15'])
        self.assertCountEqual(extract_dates('1990/6/20 11:45:45 and 17-05-1940 00:05:23'), ['1990/6/20 11:45:45', '17-05-1940 00:05:23'])
        self.assertCountEqual(extract_dates('83/06/30 4:58 and 2017-5-20 18:30'), ['83/06/30 4:58', '2017-5-20 18:30'])
        self.assertCountEqual(extract_dates('10-Dec-2020 and 7/11/2005; 06:39'), ['10-dec-2020', '7/11/2005; 06:39'])
        self.assertCountEqual(extract_dates('17-02-88 and 9-Jul-36'), ['17-02-88', '9-jul-36'])
        self.assertCountEqual(extract_dates('16/5/93; 03:45 and 7/30/1950; 8:02'), ['16/5/93; 03:45', '7/30/1950; 8:02'])
        self.assertCountEqual(extract_dates('06/17/2000; 06:42:16 and 10/13/1973'), ['06/17/2000; 06:42:16', '10/13/1973'])
        self.assertCountEqual(extract_dates('80/6/5 and 9-Apr-00 14:14:14'), ['80/6/5', '9-apr-00 14:14:14'])
        self.assertCountEqual(extract_dates('7.3.2011; 05:23:59 and 10/3/75'), ['7.3.2011; 05:23:59', '10/3/75'])
        self.assertCountEqual(extract_dates('30-09-1998 and 14.10.1938 6:02'), ['30-09-1998', '14.10.1938 6:02'])
        self.assertCountEqual(extract_dates('9-Oct-73 10:39 and 07/29/99; 04:27'), ['9-oct-73 10:39', '07/29/99; 04:27'])
        self.assertCountEqual(extract_dates('15.7.2018 and 03/17/65 17:40:39'), ['15.7.2018', '03/17/65 17:40:39'])
        self.assertCountEqual(extract_dates('1 January 1997 23:55:40, 15 April 2009; 11:34 and 09 September 1983'), ['1 january 1997 23:55:40', '15 april 2009; 11:34', '09 september 1983'])
        self.assertCountEqual(extract_dates('16 Nov 1964 8:48:01, 30 Oct 1984; 09:53 and 25 Mar 2004'), ['16 nov 1964 8:48:01', '30 oct 1984; 09:53', '25 mar 2004'])
        self.assertCountEqual(extract_dates('February 17, 2014; 10:22:40, December 25, 1998; 17:23 and June 13, 2020'), ['february 17, 2014; 10:22:40', 'december 25, 1998; 17:23', 'june 13, 2020'])

    # Tests parse_dates function
    def test_dates_parser(self):
        self.assertCountEqual(parse_dates([]), [])
        self.assertCountEqual(parse_dates(['Test']), [])
        self.assertCountEqual(parse_dates(['10-jan-2011; 22:10:15', '11-06-99 9:55:34']), [datetime(year=2011, month=1, day=10, hour=22, minute=10, second=15), datetime(year=1999, month=6, day=11, hour=9, minute=55, second=34)])
        self.assertCountEqual(parse_dates(['22-01-2006 5:44', '2003/6/9; 23:44']), [datetime(year=2006, month=1, day=22, hour=5, minute=44), datetime(year=2003, month=6, day=9, hour=23, minute=44)])
        self.assertCountEqual(parse_dates(['17/06/1975', '88/10/8']), [datetime(year=1975, month=6, day=17), datetime(year=1988, month=10, day=8)])
        self.assertCountEqual(parse_dates(['12-mar-1938 11:45', '2005-5-29']),[datetime(year=1938, month=3, day=12, hour=11, minute=45), datetime(year=2005, month=5, day=29)])
        self.assertCountEqual(parse_dates(['8/16/95', '8/09/2005 6:45:33']), [datetime(year=1995, month=8, day=16), datetime(year=2005, month=9, day=8, hour=6, minute=45, second=33)])
        self.assertCountEqual(parse_dates(['1/03/2011 19:45:04', '1958-1-2; 5:33:22']), [datetime(year=2011, month=3, day=1, hour=19, minute=45, second=4), datetime(year=1958, month=1, day=2, hour=5, minute=33, second=22)])
        self.assertCountEqual(parse_dates(['7-12-99; 8:49', '2013/8/15']), [datetime(year=1999, month=12, day=7, hour=8, minute=49), datetime(year=2013, month=8, day=15)])
        self.assertCountEqual(parse_dates(['1990/6/20 11:45:45', '17-05-1940 00:05:23']), [datetime(year=1990, month=6, day=20, hour=11, minute=45, second=45), datetime(year=1940, month=5, day=17, hour=0, minute=5, second=23)])
        self.assertCountEqual(parse_dates(['83/06/30 4:58', '2017-5-20 18:30']), [datetime(year=1983, month=6, day=30, hour=4, minute=58), datetime(year=2017, month=5, day=20, hour=18, minute=30)])
        self.assertCountEqual(parse_dates(['10-dec-2020', '7/11/2005; 06:39']), [datetime(year=2020, month=12, day=10), datetime(year=2005, month=11, day=7, hour=6, minute=39)])
        self.assertCountEqual(parse_dates(['17-02-88', '9-jul-36']), [datetime(year=1988, month=2, day=17), datetime(year=2036, month=7, day=9)])
        self.assertCountEqual(parse_dates(['16/5/93; 03:45', '7/30/1950; 8:02']), [datetime(year=1993, month=5, day=16, hour=3, minute=45), datetime(year=1950, month=7, day=30, hour=8, minute=2)])
        self.assertCountEqual(parse_dates(['06/17/2000; 06:42:16', '10/13/1973']), [datetime(year=2000, month=6, day=17, hour=6, minute=42, second=16), datetime(year=1973, month=10, day=13)])
        self.assertCountEqual(parse_dates(['80/6/5', '9-apr-00 14:14:14']), [datetime(year=1980, month=6, day=5), datetime(year=2000, month=4, day=9, hour=14, minute=14, second=14)])
        self.assertCountEqual(parse_dates(['7.3.2011; 05:23:59', '10/3/75']), [datetime(year=2011, month=3, day=7, hour=5, minute=23, second=59), datetime(year=1975, month=3, day=10)])
        self.assertCountEqual(parse_dates(['30-09-1998', '14.10.1938 6:02']), [datetime(year=1998, month=9, day=30), datetime(year=1938, month=10, day=14, hour=6, minute=2)])
        self.assertCountEqual(parse_dates(['9-oct-73 10:39', '07/29/99; 04:27']), [datetime(year=1973, month=10, day=9, hour=10, minute=39), datetime(year=1999, month=7, day=29, hour=4, minute=27)])
        self.assertCountEqual(parse_dates(['15.7.2018', '03/17/65 17:40:39']), [datetime(year=2018, month=7, day=15), datetime(year=2065, month=3, day=17, hour=17, minute=40, second=39)])
        self.assertCountEqual(parse_dates(['1 january 1997 23:55:40', '15 april 2009; 11:34', '09 september 1983']), [datetime(year=1997, month=1, day=1, hour=23, minute=55, second=40), datetime(year=2009, month=4, day=15, hour=11, minute=34), datetime(year=1983, month=9, day=9)])
        self.assertCountEqual(parse_dates(['16 nov 1964 8:48:01', '30 oct 1984; 09:53', '25 mar 2004']), [datetime(year=1964, month=11, day=16, hour=8, minute=48, second=1), datetime(year=1984, month=10, day=30, hour=9, minute=53), datetime(year=2004, month=3, day=25)])
        self.assertCountEqual(parse_dates(['february 17, 2014; 10:22:40', 'december 25, 1998; 17:23', 'june 13, 2020']), [datetime(year=2014, month=2, day=17, hour=10, minute=22, second=40), datetime(year=1998, month=12, day=25, hour=17, minute=23), datetime(year=2020, month=6, day=13)])
    
    # Tests extract_known_aliases function
    @mock.patch('controller.importer.parser.get_all_aliases')
    def test_aliases_extractor(self, mock_get_all_aliases):
        mock_get_all_aliases.return_value = []

        self.assertCountEqual(extract_known_aliases('This is a test'), [])
        self.assertCountEqual(extract_known_aliases('Double check that an empty list is returned'), [])

        mock_get_all_aliases.return_value = [AliasResult('Test', 'x'), AliasResult('alias-for-object', 'object'), AliasResult('another alias', 'object'), AliasResult('test', 'y')]

        self.assertCountEqual(extract_known_aliases('No alias to be found here'), [])
        self.assertCountEqual(extract_known_aliases('This is a test'), ['x', 'y'])
        self.assertCountEqual(extract_known_aliases('Test for extracting alias-for-object'), ['x', 'object', 'y'])
        self.assertCountEqual(extract_known_aliases('teST for x and tESt for y'), ['x', 'y'])
        self.assertCountEqual(extract_known_aliases('testing should return empty list'), [])
        self.assertCountEqual(extract_known_aliases('There is another alias for object which is ALIAS-FOR-OBJECT'), ['object'])
        self.assertCountEqual(extract_known_aliases('alias-For-OBject is being tested'), ['object'])
        self.assertCountEqual(extract_known_aliases('No such thing as another weird alias for x (test)'), ['x', 'y'])
        self.assertCountEqual(extract_known_aliases('   AnOtheR ALIas'), ['object'])
        self.assertCountEqual(extract_known_aliases('another alias   '), ['object'])
        self.assertCountEqual(extract_known_aliases('6object should return empty list'), [])
        self.assertCountEqual(extract_known_aliases('another alias is test10'), ['object'])
        self.assertCountEqual(extract_known_aliases('x'), ['x'])
        self.assertCountEqual(extract_known_aliases('x, y and alias-for-object'), ['x', 'object', 'y'])
        self.assertCountEqual(extract_known_aliases('object and y'), ['object', 'y'])

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
    @mock.patch('controller.importer.importer.parse_report')
    @mock.patch('controller.importer.importer.download_report')
    @mock.patch('controller.importer.importer.report_exists')
    def test_import_fail_error(self, mock_report_exists, mock_download_report, mock_parse_report):
        mock_report_exists.return_value = False

        mock_download_report.side_effect = NetworkError
        with self.assertRaises(ImportFailError):
            import_report(1)

        mock_download_report.side_effect = DownloadFailError
        with self.assertRaises(ImportFailError):
            import_report(1)

        mock_download_report.return_value = 'Test'
        mock_parse_report.side_effect = MissingReportElementError
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
    @mock.patch('requests_html.HTMLSession.get')
    def test_download_fail_error(self, mock_get, mock_render):
        mock_get.side_effect = None
        mock_render.side_effect = TimeoutError
        with self.assertRaises(DownloadFailError):
            download_report(1)
        
        mock_get.side_effect = Exception
        with self.assertRaises(DownloadFailError):
            download_report(1)

    # Tests that MissingReportElementError is being raised
    def test_missing_report_element_error(self):
        with self.assertRaises(MissingReportElementError):
            parse_report(1, '<Test></Test>')

        with self.assertRaises(MissingReportElementError):
            parse_report(1, '<h1 class=\'title\'></h1>')

        with self.assertRaises(MissingReportElementError):
            parse_report(1, '<h1 class=\'title\'></h1><strong></strong>')
        
        with self.assertRaises(MissingReportElementError):
            parse_report(1, '<h1 class=\'title\'></h1><strong></strong><p>Test</p><strong></strong>')

if __name__ == "__main__":
    unittest.main()