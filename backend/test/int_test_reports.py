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
from backend.model.ds.report_types import ReportResult
from datetime import datetime
from backend.model.ds.search_filters import SearchFilters
import unittest

from model.db import db_interface as db
import app

manual_import_request = {
    "import_mode": "manual",
    "atel_num": 10000
}

manual_import_request_fail = {
    "import_mode": "manual",
    "atel_num": 99999
}

class TestFR2(unittest.TestCase):
    def setup(self):
        self.app = app.test_client()

    def test_manual_import(self):
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
            reports = db.find_reports_by_object(SearchFilters(start_date=datetime(2017,1,24),end_date=datetime(2017,1,26)))
            expected = ReportResult(
                atel_num=10000,
                title="ASASSN-17bd: Discovery of A Probable Supernova in 2MASX J15591858+1336487",
                authors="J. Brimacombe (Coral Towers Observatory), J. S. Brown, K. Z. Stanek, T. W.-S. Holoien, C. S. Kochanek, J. Shields, T. A. Thompson (Ohio State), B. J. Shappee (Hubble Fellow, Carnegie Observatories), J. L. Prieto (Diego Portales; MAS), D. Bersier (LJMU), Subo Dong, S. Bose, Ping Chen (KIAA-PKU), R. A. Koff (Antelope Hills Observatory), G. Masi (Virtual Telescope Project, Ceccano, Italy), R. S. Post (Post Astronomy), G. Stone (Sierra Remote Observatories)",
                submission_date=datetime(2017,1,25,5,0),
                body=expected_body,
                keywords=["supernovae","transient"])
            self.assertTrue(expected in reports,str(reports))
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
    pass

class TestFR4:
    pass

class TestFR5:
    pass 

class TestFR6:
    pass #NYI

class TestFR7:
    pass #NYI

class TestFR8:
    pass #NYI

class TestFR9: 
    pass

class TestFR10:
    pass

class TestFR14:
    pass

class TestNFR5:
    pass

class TestNFR11:
    pass
