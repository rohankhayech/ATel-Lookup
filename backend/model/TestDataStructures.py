from datetime import datetime
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

if __name__ == '__main__':
    unittest.main()