"""
Backend integration test for report import/output requirements.

Authors:
    Rohan Khayech
    Nathan Sutardi

Contributors:
    Tully Slattery
    

License Terms and Copyright:
    Copyright (C) 2021 Rohan Khayech, Nathan Sutardi, Tully Slattery

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
from model.ds.report_types import ImportedReport, ReportResult
from datetime import datetime
from model.ds.search_filters import SearchFilters, DateFilter
import unittest
from unittest import mock

from model.db import db_interface as db
from app import app

manual_import_request = {
    "import_mode": "manual",
    "atel_num": 10000
}

manual_import_request_fail = {
    "import_mode": "manual",
    "atel_num": 99999
}

manual_import_request_fail_two = {
    "import_mode": "manual",
    "atel_num": 6079
}

class TestFR2(unittest.TestCase):
    """
    The software must allow an administrator to import new reports by ATel number from The Astronomer’s Telegram website into the database.

    If the ATel exists, complete database entry for the report is created and user informed of successful entry. If the ATel does not exist, display an error message to the user.
    """
    def setUp(self):
        self.app = app.test_client()

    @mock.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    def test_manual_import(self, verify_jwt_in_request):
        verify_jwt_in_request.return_value = True

        # Delete report if already exists
        cn = db._connect()
        cur = cn.cursor()
        cur.execute("delete from Reports where atelNum = 10000")
        cur.close()
        cn.commit()
        cn.close()

        # Send import request
        response = self.app.post('/import', json=manual_import_request)
        
        # Check response flag
        self.assertEqual(response.json.get("flag"), 1)

        # Check report exists
        self.assertTrue(db.report_exists(10000))

        # Retrieves ATel #10000 body text
        f = open(os.path.join('test', 'res', 'atel10000_body.txt'), 'r')
        expected_body = f.read()
        f.close()

        try:
            # Check report attributes
            reports = db.find_reports_by_object(SearchFilters(term="A"),DateFilter(start_date=datetime(2017,1,24),end_date=datetime(2017,1,26)))
            expected = ReportResult(
                atel_num=10000,
                title="ASASSN-17bd: Discovery of A Probable Supernova in 2MASX J15591858+1336487",
                authors="J. Brimacombe (Coral Towers Observatory), J. S. Brown, K. Z. Stanek, T. W.-S. Holoien, C. S. Kochanek, J. Shields, T. A. Thompson (Ohio State), B. J. Shappee (Hubble Fellow, Carnegie Observatories), J. L. Prieto (Diego Portales; MAS), D. Bersier (LJMU), Subo Dong, S. Bose, Ping Chen (KIAA-PKU), R. A. Koff (Antelope Hills Observatory), G. Masi (Virtual Telescope Project, Ceccano, Italy), R. S. Post (Post Astronomy), G. Stone (Sierra Remote Observatories)",
                submission_date=datetime(2017,1,25,5,0),
                body=expected_body)
            self.assertNotEqual(reports,[])
            self.assertTrue(expected in reports, str(reports))
        finally:
            # Delete report
            cn = db._connect()
            cur = cn.cursor()
            cur.execute("delete from Reports where atelNum = 10000")
            cur.close()
            cn.commit()
            cn.close()

    @mock.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    def test_manual_import_fail(self, verify_jwt_in_request):
        verify_jwt_in_request.return_value = True

        # Delete reports if already exist
        cn = db._connect()
        cur = cn.cursor()
        cur.execute("delete from Reports where atelNum = 10000")
        cur.execute("delete from Reports where atelNum = 99999")
        cur.execute("delete from Reports where atelNum = 6079")
        cur.close()
        cn.commit()
        cn.close()

        # ReportAlreadyExistsError
        # Send import request
        response = self.app.post('/import', json=manual_import_request)
        self.assertEqual(response.json.get("flag"), 1)

        # Check report exists
        self.assertTrue(db.report_exists(10000))

        # Send same import request
        response = self.app.post('/import', json=manual_import_request)

        # Check response flag
        self.assertEqual(response.json.get("flag"), 2)
        
        # Check an error message has been returned
        message = response.json.get("message")
        self.assertIsNotNone(message)
        self.assertNotEqual(message, "")

        # ReportNotFoundError
        # Send import request
        response = self.app.post('/import', json=manual_import_request_fail)

        # Check response flag
        self.assertEqual(response.json.get("flag"), 2)

        # Check report exists
        self.assertFalse(db.report_exists(99999))

        # MissingReportElementError
        # Send import request
        response = self.app.post('/import', json=manual_import_request_fail_two)

        # Check response flag
        self.assertEqual(response.json.get("flag"), 0)

        # Check report exists
        self.assertFalse(db.report_exists(6079))

        # Delete reports
        cn = db._connect()
        cur = cn.cursor()
        cur.execute("delete from Reports where atelNum = 10000")
        cur.execute("delete from Reports where atelNum = 99999")
        cur.execute("delete from Reports where atelNum = 6079")
        cur.close()
        cn.commit()
        cn.close()

class TestFR3:
    pass #NYI

manual_import_request_two = {
    "import_mode": "manual",
    "atel_num": 12000
}

manual_import_request_three = {
    "import_mode": "manual",
    "atel_num": 14000
}

search_by_name_request = {
    "term": "",
    "search_mode": "name",
    "search_data": "IGR J17591-2342",
    "keywords": [],
    "keyword_mode": "none",
    "start_date": "",
    "end_date": ""
}

class TestFR4_NFR1_NFR2(unittest.TestCase):
    """
    The software must categorise imported ATels based on predefined keywords, observation dates, known aliases, object coordinates and referenced ATels.

    The software will parse the title and body text for any terms matching predefined keywords, known aliases or common formats for dates, ATel references and coordinates (in common representations of both decimal degrees and sexagesimal formats). 
    If coordinates are found the system must query SIMBAD for the object and its aliases and add these to the database. 
    The report is then categorised with all extracted fields, before being saved in the database.

    The software must sanitise the title and body fields parsed from ATel source files prior to entering these fields into the database or displaying these fields on any page of the website. 
    All script and other HTML tags must be removed and any special characters that could be used in an SQL injection attack must be escaped.
    """
    def setUp(self):
        self.app = app.test_client()

    @mock.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    def test_categorisation(self, verify_jwt_in_request):
        verify_jwt_in_request.return_value = True

        # Delete records if already exist
        cn = db._connect()
        cur = cn.cursor()
        cur.execute("delete from Reports where atelNum = 12000")
        cur.execute("delete from ReportRefs where atelNum = 12000")
        cur.execute("delete from ReportRefs where refReport = 12000")
        cur.execute("delete from Reports where atelNum = 14000")
        cur.execute("delete from ReportRefs where atelNum = 14000")
        cur.execute("delete from ReportRefs where refReport = 14000")
        cur.execute("delete from Objects where objectID = 'IGR J17591-2342'")
        cur.close()
        cn.commit()
        cn.close()

        # Send import request for ATel #12000
        response = self.app.post('/import', json=manual_import_request_two)
        self.assertEqual(response.json.get("flag"), 1)

        # Send import request for ATel #14000
        response = self.app.post('/import', json=manual_import_request_three)
        self.assertEqual(response.json.get("flag"), 1)

        # Send search request
        response = self.app.post('/search', json=search_by_name_request)
        self.assertEqual(response.json.get("flag"), 1)

        # Check report exists
        self.assertTrue(db.report_exists(12000))
        self.assertTrue(db.report_exists(14000))

        # Retrieves ATel #12000 body text
        f = open(os.path.join('test', 'res', 'atel12000_body.txt'), 'r')
        expected_body_12000 = f.read()
        f.close()

        # Retrieves ATel #14000 body text
        f = open(os.path.join('test', 'res', 'atel14000_body.txt'), 'r')
        expected_body_14000 = f.read()
        f.close()

        # This test NFR1 and NFR2 as well
        try:
            cn = db._connect()
            cur = cn.cursor()

            # ATel #12000
            # Test ATel number
            cur.execute("select atelNum from Reports where atelNum = 12000")
            result = cur.fetchall()[0]
            self.assertEqual(result, (12000,))

            # Test title
            cur.execute("select title from Reports where atelNum = 12000")
            result = cur.fetchall()[0]
            self.assertEqual(result, ("INTEGRAL detects a rebrightening of the accreting millisecond X-ray pulsar IGR J17591-2342",))

            # Test authors
            cur.execute("select authors from Reports where atelNum = 12000")
            result = cur.fetchall()[0]
            self.assertEqual(result, ("C. Sanchez-Fernandez (ESAC, ESA), C. Ferrigno, J. Chenevez, E. Kuulkers, R. Wijnands, A. Bazzano, P. Jonker, M. Del Santo, on behalf of the INTEGRAL Galactic bulge monitoring team",))

            # Test body
            cur.execute("select body from Reports where atelNum = 12000")
            result = cur.fetchall()[0]
            self.assertEqual(result, (expected_body_12000,))

            # Test submission date
            cur.execute("select submissionDate from Reports where atelNum = 12000")
            result = cur.fetchall()[0]
            self.assertEqual(result, (datetime(year=2018, month=9, day=1, hour=11, minute=24),))

            # Test keywords
            cur.execute("select keywords from Reports where atelNum = 12000")
            result = cur.fetchall()[0]
            self.assertEqual(result, ({"x-ray",
                                       "gamma ray",
                                       "binary",
                                       "neutron star",
                                       "pulsar",
                                       "star",
                                       "transient"
            },))

            # Test referenced reports
            cur.execute("select refReport from ReportRefs where atelNum = 12000")
            results = cur.fetchall()
            self.assertCountEqual(results, [(11941,), (11981,), (11957,)])

            # Test referenced by reports
            cur.execute("select atelNum from ReportRefs where refReport = 12000")
            results = cur.fetchall()
            self.assertCountEqual(results, [(12004,)])

            # Test observation dates
            cur.execute("select obdate from ObservationDates where atelNumFK = 12000")
            results = cur.fetchall()
            self.assertCountEqual(results, [(datetime(2018, 8, 11),), (datetime(2018, 7, 22),)])

            # Test object IDs
            cur.execute("select objectIDFK from ObjectRefs where atelNumFK = 12000")
            results = cur.fetchall()
            self.assertCountEqual(results, [("IGR J17591-2342",)])

            # Test coordinates
            cur.execute("select ra, declination from ReportCoords where atelNumFK = 12000")
            results = cur.fetchall()
            self.assertCountEqual(results, [])

            # ATel #14000
            # Test ATel number
            cur.execute("select atelNum from Reports where atelNum = 14000")
            result = cur.fetchall()[0]
            self.assertEqual(result, (14000,))

            # Test title
            cur.execute("select title from Reports where atelNum = 14000")
            result = cur.fetchall()[0]
            self.assertEqual(result, ("Optical polarization of AT2019wey",))

            # Test authors
            cur.execute("select authors from Reports where atelNum = 14000")
            result = cur.fetchall()[0]
            self.assertEqual(result, ("F. Bouzelou(Univ. of Crete, Greece), S. Kiehlmann (IA FORTH & Univ. of Crete, Greece), L. Markopoulioti (Univ. of Crete, Greece)",))

            # Test body
            cur.execute("select body from Reports where atelNum = 14000")
            result = cur.fetchall()[0]
            self.assertEqual(result, (expected_body_14000,))

            # Test submission date
            cur.execute("select submissionDate from Reports where atelNum = 14000")
            result = cur.fetchall()[0]
            self.assertEqual(result, (datetime(year=2020, month=9, day=8, hour=19, minute=5),))

            # Test keywords
            cur.execute("select keywords from Reports where atelNum = 14000")
            result = cur.fetchall()[0]
            self.assertEqual(result, ({"radio",
                                       "optical",
                                       "x-ray",
                                       "agn",
                                       "binary",
                                       "blazar",
                                       "star",
                                       "transient"
            },))

            # Test referenced reports
            cur.execute("select refReport from ReportRefs where atelNum = 14000")
            results = cur.fetchall()
            self.assertCountEqual(results, [(13571,), (13576,), (13932,), (13921,), (13948,), (13957,), (13976,), (13984,)])

            # Test referenced by reports
            cur.execute("select atelNum from ReportRefs where refReport = 14000")
            results = cur.fetchall()
            self.assertCountEqual(results, [(14003,), (14100,), (14168,)])

            # Test observation dates
            cur.execute("select obdate from ObservationDates where atelNumFK = 14000")
            results = cur.fetchall()
            self.assertCountEqual(results, [(datetime(2020, 5, 27),), (datetime(2020, 9, 6),)])

            # Test object IDs
            cur.execute("select objectIDFK from ObjectRefs where atelNumFK = 14000")
            results = cur.fetchall()
            self.assertCountEqual(results, [])

            # Test coordinates
            cur.execute("select ra, declination from ReportCoords where atelNumFK = 14000")
            results = cur.fetchall()

            result = results[0]
            self.assertAlmostEqual(float(result[0]), 68.7687500000, 10)
            self.assertAlmostEqual(float(result[1]), 55.3577777778, 10)

            result = results[1]
            self.assertAlmostEqual(float(result[0]), 68.8562500000, 10)
            self.assertAlmostEqual(float(result[1]), 55.3919444444, 10)

            # Object
            # Test object's properties
            cur.execute("select ra, declination from Objects where objectID = \'IGR J17591-2342\'")
            result = cur.fetchall()[0]
            self.assertAlmostEqual(float(result[0]), 269.7866208333, 10)
            self.assertAlmostEqual(float(result[1]), -23.7129722222, 10)

            # Test object's aliases
            cur.execute("select alias from Aliases where objectIDFK = \'IGR J17591-2342\'")
            results = cur.fetchall()
            self.assertCountEqual(results, [("IGR J17591-2342",)])

            cur.close()
            cn.close()
        finally:
            # Delete all records
            cn = db._connect()
            cur = cn.cursor()
            cur.execute("delete from Reports where atelNum = 12000")
            cur.execute("delete from ReportRefs where atelNum = 12000")
            cur.execute("delete from ReportRefs where refReport = 12000")
            cur.execute("delete from Reports where atelNum = 14000")
            cur.execute("delete from ReportRefs where atelNum = 14000")
            cur.execute("delete from ReportRefs where refReport = 14000")
            cur.execute("delete from Objects where objectID = \'IGR J17591-2342\'")
            cur.close()
            cn.commit()
            cn.close()

all_keyword_search_request = {
    "term": "",
    "search_data": "",
    "search_mode": "name",
    "keywords": ["transient", "supernovae"],
    "keyword_mode": "all",
    "start_date": "",
    "end_date": ""
}

any_keyword_search_request = {
    "term": "",
    "search_data": "",
    "search_mode": "name",
    "keywords": ["transient", "supernovae"],
    "keyword_mode": "any",
    "start_date": "",
    "end_date": ""
}

none_keyword_search_request = {
    "term": "",
    "search_data": "",
    "search_mode": "name",
    "keywords": ["transient", "supernovae"],
    "keyword_mode": "none",
    "start_date": "",
    "end_date": ""
}

class TestFR5(unittest.TestCase):
    """
    The software must allow the user to search for ATels by keyword.
    The software returns a list of all the ATels categorised with/without the selected keywords, depending on search mode.
    """
    def setUp(self):
        self.app = app.test_client()

    def test_search_by_keyword(self):
        all_report = db.add_report(ImportedReport(20000,"T","A","B",datetime(2021,1,1),keywords=['transient','supernovae']))
        any_report1 = db.add_report(ImportedReport(20001, "T", "A", "B", datetime(2021, 1, 1), keywords=['supernovae']))
        any_report2 = db.add_report(ImportedReport(20002, "T", "A", "B", datetime(2021, 1, 1), keywords=['transient']))
        none_report = db.add_report(ImportedReport(20003,"T","A","B",datetime(2021,1,1),keywords=[]))

        try:
            # Send all search request
            response = self.app.post('/search', json=all_keyword_search_request)

            reports = response.json.get("report_list")
            self.assertIn({
                "atel_num": 20000,
                "authors": "A",
                "body": "B",
                "referenced_reports": [],
                "submission_date": "2021-01-01 00:00:00",
                "title": "T"
            }, reports)

            # Send any search request
            response = self.app.post(
                '/search', json=any_keyword_search_request)

            reports = response.json.get("report_list")
            self.assertIn({
                "atel_num": 20000,
                "authors": "A",
                "body": "B",
                "referenced_reports": [],
                "submission_date": "2021-01-01 00:00:00",
                "title": "T"
            }, reports)
            self.assertIn({
                "atel_num": 20001,
                "authors": "A",
                "body": "B",
                "referenced_reports": [],
                "submission_date": "2021-01-01 00:00:00",
                "title": "T"
            }, reports)
            self.assertIn({
                "atel_num": 20002,
                "authors": "A",
                "body": "B",
                "referenced_reports": [],
                "submission_date": "2021-01-01 00:00:00",
                "title": "T"
            }, reports)

            # Send none request
            response = self.app.post(
                '/search', json=none_keyword_search_request)

            reports = response.json.get("report_list")
            self.assertIn({
                "atel_num": 20003,
                "authors": "A",
                "body": "B",
                "referenced_reports": [],
                "submission_date": "2021-01-01 00:00:00",
                "title": "T"
            }, reports)
        finally:
            # Delete reports
            cn = db._connect()
            cur = cn.cursor()
            cur.execute("delete from Reports where atelNum = 20000")
            cur.execute("delete from Reports where atelNum = 20001")
            cur.execute("delete from Reports where atelNum = 20002")
            cur.execute("delete from Reports where atelNum = 20003")
            cur.close()
            cn.commit()
            cn.close()    

term_search_request = {
    "term": "db_test_term",
    "search_mode": "name",
    "search_data": "",
    "keywords": [],
    "keyword_mode": "any",
    "start_date": "",
    "end_date": ""
}

class TestFR9(unittest.TestCase):
    """
    The software must allow the user to search for ATels by free text.
    The user inputs a free-text search string.
    The software returns a list of all the ATels containing the search string in the title and/or body.
    """
    def setUp(self):
        self.app = app.test_client()

    def test_search_by_term(self):
        title_report = db.add_report(ImportedReport(20000,"db_test_term_title","A","B",datetime(2021,1,1)))
        body_report1 = db.add_report(ImportedReport(20001, "T", "A", "db_test_term_body", datetime(2021, 1, 1)))

        try:
            # Send all search request
            response = self.app.post(
                '/search', json=term_search_request)

            reports = response.json.get("report_list")
            self.assertIn({
                "atel_num": 20000,
                "authors": "A",
                "body": "B",
                "referenced_reports": [],
                "submission_date": "2021-01-01 00:00:00",
                "title": "db_test_term_title"
            }, reports)
            self.assertIn({
                "atel_num": 20001,
                "authors": "A",
                "body": "db_test_term_body",
                "referenced_reports": [],
                "submission_date": "2021-01-01 00:00:00",
                "title": "T"
            }, reports)
        finally:
            # Delete reports
            cn = db._connect()
            cur = cn.cursor()
            cur.execute("delete from Reports where atelNum = 20000")
            cur.execute("delete from Reports where atelNum = 20001")
            cur.close()
            cn.commit()
            cn.close()

class TestFR10:
    pass #NYI

class TestFR14:
    pass #NYI

if __name__ == '__main__':
    unittest.main()