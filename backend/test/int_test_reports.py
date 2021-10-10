"""
Backend integration test for report import/output requirements.

Author:
    Rohan Khayech

Contributors:
    Tully Slattery
    Nathan Sutardi

License Terms and Copyright:
    Copyright (C) 2021 Rohan Khayech, Tully Slattery, Nathan Sutardi

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

class TestFR2(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_manual_import(self):

        #delete report if already exists
        cn = db._connect()
        cur = cn.cursor()
        cur.execute("delete from Reports where atelNum = 10000")
        cur.close()
        cn.commit()
        cn.close()

        #send import request
        response = self.app.post('/import', json=manual_import_request)
        
        #Check response flag
        self.assertEqual(response.json.get("flag"), 1)

        #check report exists
        self.assertTrue(db.report_exists(10000))

        # Retrieves ATel #10000 body text
        f = open(os.path.join('test', 'res', 'atel10000_body.txt'), 'r')
        expected_body = f.read()
        f.close()

        try:
            #check report attributes
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
            #delete report
            cn = db._connect()
            cur = cn.cursor()
            cur.execute("delete from Reports where atelNum = 10000")
            cur.close()
            cn.commit()
            cn.close()

    def test_manual_import_fail(self):
        #send import request
        response = self.app.post('/import', json=manual_import_request_fail)

        #Check response flag
        self.assertEqual(response.json.get("flag"), 0)

        #check report exists
        self.assertFalse(db.report_exists(99999))

class TestFR3:
    pass #NYI

class TestFR4:
    pass #NYI

all_keyword_search_request = {
    "search_mode": "name",
    "keywords": ["transient", "supernovae"],
    "keyword_mode": "all",
}

any_keyword_search_request = {
    "search_mode": "name",
    "keywords": ["transient", "supernovae"],
    "keyword_mode": "any",
}

none_keyword_search_request = {
    "search_mode": "name",
    "keywords": ["transient", "supernovae"],
    "keyword_mode": "none",
}

class TestFR5(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_search_by_keyword(self):
        all_report = db.add_report(ImportedReport(20000,"T","A","B",datetime(2021,1,1),keywords=['transient','supernovae']))
        any_report1 = db.add_report(ImportedReport(20001, "T", "A", "B", datetime(2021, 1, 1), keywords=['supernovae']))
        any_report2 = db.add_report(ImportedReport(20002, "T", "A", "B", datetime(2021, 1, 1), keywords=['transient']))
        none_report = db.add_report(ImportedReport(20003,"T","A","B",datetime(2021,1,1),keywords=[]))

        try:
            #send all search request
            response = self.app.post('/search', json=all_keyword_search_request)

            #raise ValueError(str(response.json))

            reports = response.json.get("report_list")
            self.assertIn({
                "atel_num": 20000,
                "authors": "A",
                "body": "B",
                "referenced_reports": [],
                "submission_date": "2021-01-01 00:00:00",
                "title": "T"
            }, reports)

            #send any search request
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

            #send none request
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
            #delete reports
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
}

class TestFR9(unittest.TestCase): 
    def setUp(self):
        self.app = app.test_client()

    def test_search_by_term(self):
        title_report = db.add_report(ImportedReport(20000,"db_test_term_title","A","B",datetime(2021,1,1)))
        body_report1 = db.add_report(ImportedReport(20001, "T", "A", "db_test_term_body", datetime(2021, 1, 1)))

        try:
            #send all search request
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
            #delete reports
            cn = db._connect()
            cur = cn.cursor()
            cur.execute("delete from Reports where atelNum = 20000")
            cur.execute("delete from Reports where atelNum = 20001")
            cur.close()
            cn.commit()
            cn.close()

class TestFR14:
    pass #NYI


if __name__ == '__main__':
    unittest.main()
