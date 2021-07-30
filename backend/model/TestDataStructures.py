from datetime import datetime

from astropy.coordinates.sky_coordinate import SkyCoord
from SearchFilters import KeywordMode
from SearchFilters import SearchFilters
from ReportTypes import ReportResult, ImportedReport
from DBHelper import AliasResult
import unittest

class TestAliasResult(unittest.TestCase):
    
    #Setup
    def setUp(self):
        self.ar = AliasResult("Name","OBJ")

    #Test constructor
    def test_creation(self):
        self.assertEqual(self.ar._alias,"Name")
        self.assertEqual(self.ar._object_ID, "OBJ")

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

class TestSearchFilters(unittest.TestCase):
    def setUp(self):
        self.sf = SearchFilters("term",["key", "word"],KeywordMode.ALL,datetime(2021,7,30),datetime(2021,7,31))

    #test regular creation, setters
    def test_creation(self):
        self.assertEqual(self.sf._term, "term")
        self.assertListEqual(self.sf._keywords, ["key", "word"])
        self.assertEqual(self.sf._keyword_mode, KeywordMode.ALL)
        self.assertEqual(self.sf._start_date, datetime(2021,7,30))
        self.assertEqual(self.sf._end_date, datetime(2021,7,31))

    #test with only term, defaults
    def test_creation_only_term(self):
        sf2 = SearchFilters("term")
        self.assertEqual(sf2._term, "term")
        self.assertIsNone(sf2._keywords)
        self.assertEqual(sf2._keyword_mode, KeywordMode.ANY)
        self.assertIsNone(sf2._start_date)
        self.assertIsNone(sf2._end_date)
        
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
        self.assertEqual(self.sf.start_date, datetime(2021,7,30))
        self.assertEqual(self.sf.end_date, datetime(2021,7,31))

    #test kw mode enum setter
    def test_enum(self):
        for i in range(0,3):
            self.sf.keyword_mode = KeywordMode(i)
            self.assertEqual(self.sf._keyword_mode,KeywordMode(i))
        with self.assertRaises(TypeError):
            self.sf.keyword_mode = 5

class TestReportTypes(unittest.TestCase):
    def setUp(self):
        self.ir = ImportedReport(14000, "ATel Title", "R. Khayech", "Body text", datetime(2021,7,30), [14001], [datetime(2021,8,30)], ["key", "words"], ["X1"], [], [13000])

    #test creation, setters
    def test_creation(self):
        self.assertEqual(self.ir._atel_num, 14000)
        self.assertEqual(self.ir._title, "ATel Title")
        self.assertEqual(self.ir._authors, "R. Khayech")
        self.assertEqual(self.ir._body, "Body text")
        self.assertEqual(self.ir._submission_date, datetime(2021,7,30))
        self.assertListEqual(self.ir._referenced_reports, [14001])
        self.assertListEqual(self.ir._observation_dates, [datetime(2021,8,30)])
        self.assertListEqual(self.ir._keywords, ["key", "words"])
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
        self.assertListEqual(self.ir.keywords, ["key", "words"])
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

    def test_invalid_atel_num(self):
        with self.assertRaises(ValueError):
            self.ir.atel_num = 0

    def test_invalid_body_len(self):
        with self.assertRaises(ValueError):
            self.ir.body = "a"*4001

if __name__ == '__main__':
    unittest.main()