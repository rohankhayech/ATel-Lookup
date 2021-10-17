"""
Test suite for all local data structures.

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

from datetime import datetime
import unittest

from astropy.coordinates.sky_coordinate import SkyCoord

from model.ds.alias_result import AliasResult
from model.ds.search_filters import SearchFilters, DateFilter, KeywordMode
from model.ds.report_types import ImportedReport, ReportResult
from model.constants import valid_keyword

class TestAliasResult(unittest.TestCase):
    
    #Setup
    def setUp(self):
        self.ar = AliasResult("Name","OBJ")

    #Test constructor
    def test_creation(self):
        self.assertEqual(self.ar._alias,"Name")
        self.assertEqual(self.ar._object_ID, "OBJ")

    #Test type conversion/checking
    def test_type_safety(self):
        ar2 = AliasResult(1,2)
        self.assertEqual(ar2._alias,"1")
        self.assertEqual(ar2._object_ID,"2")

    #Test getters
    def test_getters(self):
        self.assertEqual(self.ar.alias,"Name")
        self.assertEqual(self.ar.object_ID,"OBJ")

    #Test immutability
    def test_setters(self):
        with self.assertRaises(TypeError):
            self.ar.alias = "Name 2"
        with self.assertRaises(TypeError):
            self.ar.object_ID = "Name"
        self.assertEqual(self.ar._alias,"Name")
        self.assertEqual(self.ar._object_ID, "OBJ")

    def test_equal(self):
        ar2 = AliasResult("Name", "OBJ")
        self.assertEqual(self.ar, ar2)

        ar3 = AliasResult("Name","obj")
        self.assertNotEqual(self.ar, ar3)

        ar4 = AliasResult("name","OBJ")
        self.assertNotEqual(self.ar, ar4)

class TestSearchFilters(unittest.TestCase):
    def setUp(self):
        self.sf = SearchFilters("term",["key", "word"],KeywordMode.ALL)
        self.df = DateFilter(datetime(2021,7,30),datetime(2021,7,31))

    #test regular creation, setters
    def test_creation(self):
        self.assertEqual(self.sf._term, "term")
        self.assertListEqual(self.sf._keywords, ["key", "word"])
        self.assertEqual(self.sf._keyword_mode, KeywordMode.ALL)
        self.assertEqual(self.df._start_date, datetime(2021,7,30))
        self.assertEqual(self.df._end_date, datetime(2021,7,31))

    #test with only term, defaults
    def test_creation_only_term(self):
        sf2 = SearchFilters("term")
        self.assertEqual(sf2._term, "term")
        self.assertIsNone(sf2._keywords)
        self.assertEqual(sf2._keyword_mode, KeywordMode.ANY)

    def test_keywords_none_getter(self):
        sf2 = SearchFilters("term")
        self.assertIsNone(sf2.keywords)
        
    #test with only keywords
    def test_only_keywords(self):
        sf2 = SearchFilters(keywords=["key","word"])

    #test fails with empty keywords
    def test_empty_keywords(self):
        with self.assertRaises(TypeError):
            sf2 = SearchFilters(keywords=[])

    #test fails with no args
    def test_no_args(self):
        with self.assertRaises(TypeError):
            sf2 = SearchFilters()

    #test getters
    def test_getters(self):
        self.assertEqual(self.sf.term, "term")
        self.assertListEqual(self.sf.keywords, ["key", "word"])
        self.assertEqual(self.sf.keyword_mode, KeywordMode.ALL)
        self.assertEqual(self.df.start_date, datetime(2021,7,30))
        self.assertEqual(self.df.end_date, datetime(2021,7,31))

        self.sf.term = None
        self.assertIsNone(self.sf.term)

    #test type conversion/safety
    def test_type_safety(self):
        self.sf.term = 1
        self.assertEqual(self.sf.term, "1")
        with self.assertRaises(TypeError):
            self.sf.keywords = [1]
        with self.assertRaises(TypeError):
            self.df.start_date = 1
        with self.assertRaises(TypeError):
            self.df.end_date = 1

    #test kw mode enum setter
    def test_enum(self):
        for i in range(0,3):
            self.sf.keyword_mode = KeywordMode(i)
            self.assertEqual(self.sf._keyword_mode,KeywordMode(i))
        with self.assertRaises(TypeError):
            self.sf.keyword_mode = 5

    def testEquals(self):
        sf2 = SearchFilters("term",["key", "word"],KeywordMode.ALL)
        df2 = DateFilter(datetime(2021, 7, 30), datetime(2021, 7, 31))
        self.assertEqual(self.sf, sf2)
        self.assertEqual(self.df, df2)

        # test not equal
        sf3 = SearchFilters("term",["key","word"],KeywordMode.ANY)
        self.assertNotEqual(self.sf, sf3)

class TestReportTypes(unittest.TestCase):
    def setUp(self):
        self.ir = ImportedReport(14000, "ATel Title", "R. Khayech", "Body text", datetime(2021,7,30), [14001], [datetime(2021,8,30)], ["Radio", "sTAR"], ["X1"], [], [13000])

    #test creation, setters
    def test_creation(self):
        self.assertEqual(self.ir._atel_num, 14000)
        self.assertEqual(self.ir._title, "ATel Title")
        self.assertEqual(self.ir._authors, "R. Khayech")
        self.assertEqual(self.ir._body, "Body text")
        self.assertEqual(self.ir._submission_date, datetime(2021,7,30))
        self.assertListEqual(self.ir._referenced_reports, [14001])
        self.assertListEqual(self.ir._observation_dates, [datetime(2021,8,30)])
        self.assertListEqual(self.ir._keywords, ["Radio", "sTAR"])
        self.assertListEqual(self.ir._objects, ["X1"])
        self.assertListEqual(self.ir._coordinates, [])
        self.assertListEqual(self.ir._referenced_by, [13000])

    #test getters
    def test_getters(self):
        self.assertEqual(self.ir.atel_num, 14000)
        self.assertEqual(self.ir.title, "ATel Title")
        self.assertEqual(self.ir.authors, "R. Khayech")
        self.assertEqual(self.ir.body, "Body text")
        self.assertEqual(self.ir.submission_date, datetime(2021,7,30))
        self.assertListEqual(self.ir.referenced_reports, [14001])
        self.assertListEqual(self.ir.observation_dates, [datetime(2021,8,30)])
        self.assertListEqual(self.ir.keywords, ["Radio", "sTAR"])
        self.assertListEqual(self.ir.objects, ["X1"])
        self.assertListEqual(self.ir.coordinates, [])
        self.assertListEqual(self.ir.referenced_by, [13000])

    def test_defaults(self):
        ir2 = ImportedReport(14000, "ATel Title", "R. Khayech", "Body text", datetime(2021,7,30))
        self.assertEqual(ir2._atel_num, 14000)
        self.assertEqual(ir2._title, "ATel Title")
        self.assertEqual(ir2._authors, "R. Khayech")
        self.assertEqual(ir2._body, "Body text")
        self.assertEqual(ir2._submission_date, datetime(2021,7,30))
        self.assertListEqual(ir2._referenced_reports, [])
        self.assertListEqual(ir2._observation_dates, [])
        self.assertListEqual(ir2._keywords, [])
        self.assertListEqual(ir2._objects, [])
        self.assertListEqual(ir2._coordinates, [])
        self.assertListEqual(ir2._referenced_by, [])

    def test_equals(self):
        rr = ReportResult(14000, "ATel Title", "R. Khayech", "Body text", datetime(2021, 7, 30), [14001])
        ir2 = ImportedReport(14000, "ATel Title", "R. Khayech", "Body text", datetime(2021, 7, 30), [14001], [datetime(2021, 8, 30)], ["Radio", "sTAR"], ["X1"], [], [13000])

        self.assertEqual(self.ir,rr)
        self.assertEqual(self.ir,ir2)

        ir3 = ImportedReport(14000, "ATel Title", "R. Khayech", "Body", datetime(2021, 7, 30), [14001], [datetime(2021, 8, 30)], ["Radio", "sTAR"], ["X1"], [], [13000])
        self.assertNotEqual(self.ir,ir3)

        ir4 = ImportedReport(14000, "ATel Title", "R. Khayech", "Body text", datetime(2021, 7, 30), [14001], [datetime(2021, 8, 30)], ["Radio", "sTAR"], [], [], [13000])
        self.assertNotEqual(self.ir,ir4)

    def test_invalid_atel_num(self):
        with self.assertRaises(ValueError):
            self.ir.atel_num = 0

    def test_invalid_lens(self):
        self.ir.body = "a"*5120  # Allow minor invalid lengths
        with self.assertRaises(ValueError):
            self.ir.body = "a"*5121
        with self.assertRaises(ValueError):
            self.ir.title = "a"*2057
        with self.assertRaises(ValueError):
            self.ir.authors = "a"*8193

    def test_invalid_keyword(self):
        with self.assertRaises(ValueError):
            self.ir.keywords = ["test"]

    #Test type conversion/checking
    def test_type_safety(self):
        with self.assertRaises(TypeError):
            self.ir.atel_num = "str"
        self.ir.title = 1
        self.assertEqual(self.ir.title, "1")
        self.ir.authors = 1
        self.assertEqual(self.ir.authors, "1")
        self.ir.body = 1
        self.assertEqual(self.ir.body, "1")
        with self.assertRaises(TypeError):
            self.ir.submission_date = 1
        with self.assertRaises(TypeError):
            self.ir.coordinates = [1]
        with self.assertRaises(TypeError):
            self.ir.keywords = [1]
        with self.assertRaises(TypeError):
            self.ir.objects = [1]
        with self.assertRaises(TypeError):
            self.ir.observation_dates = [1]
        with self.assertRaises(TypeError):
            self.ir.referenced_by = ["str"]
        with self.assertRaises(TypeError):
            self.ir.referenced_reports = ["str"]

class TestConstants(unittest.TestCase):
    def testValid(self):
        self.assertTrue(valid_keyword("Radio"))
        self.assertTrue(valid_keyword("request for observations"))
        self.assertTrue(valid_keyword("sTAR"))
    
    def testInvalid(self):
        self.assertFalse(valid_keyword("test"))

if __name__ == '__main__':
    unittest.main()
