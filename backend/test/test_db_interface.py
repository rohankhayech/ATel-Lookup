"""
Test suite for the database helper module. 

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
import unittest
from datetime import datetime

import mysql.connector
from mysql.connector.cursor import MySQLCursor
from astropy.coordinates.sky_coordinate import SkyCoord

from model.db import db_interface as db
from model.ds.alias_result import AliasResult
from model.ds.report_types import ImportedReport
from model.ds.search_filters import DateFilter, KeywordMode, SearchFilters



class TestInitTables(unittest.TestCase):
    #Verify tables exist/were created on container init
    def testTables(self):
        _verifyTable(self,"AdminUsers")
        _verifyTable(self, "Reports")
        _verifyTable(self,"Metadata")
        _verifyTable(self,"Objects")
        _verifyTable(self,"Aliases")
        _verifyTable(self,"ObjectRefs")

def _verifyTable(self:TestInitTables, table_name):
    cn = db._connect()
    cur:MySQLCursor = cn.cursor()

    cur.execute(f"show tables like '{table_name}'")

    result = cur.fetchone()

    cur.close()
    cn.close()

    self.assertTrue(result)

class TestAuth(unittest.TestCase):
    
    def testAddUser(self):
        db.add_admin_user("test","hash")
        self.assertTrue(db.user_exists("test"))
    
    def testDupeUser(self):
        db.add_admin_user("test", "hash")
        with (self.assertRaises(db.ExistingUserError)):
            db.add_admin_user("test","hash")

    def testUserNotExists(self):
        self.assertFalse(db.user_exists("test2"))

    def testGetPassword(self):
        db.add_admin_user("test", "hash")
        self.assertEqual(db.get_hashed_password("test"),"hash")
        with (self.assertRaises(db.UserNotFoundError)):
            db.get_hashed_password("test2")

    def testExceedsMax(self):
        with (self.assertRaises(ValueError)):
            db.add_admin_user("a"*26,"hash")
        with (self.assertRaises(ValueError)):
            db.add_admin_user("test","a"*256)
        with (self.assertRaises(ValueError)):
            db.add_admin_user("","hash")
        with (self.assertRaises(ValueError)):
            db.add_admin_user("test","")

    def tearDown(self):
        #remove test user
        cn = db._connect()
        cur:MySQLCursor = cn.cursor()
        cur.execute("delete from AdminUsers where username = 'test'")
        cur.close()
        cn.commit()
        cn.close()

class TestReports(unittest.TestCase):
    def setUp(self):
        pass

    def testNextATelNum(self):
        #set up
        old_num = db.get_next_atel_num()

        db.set_next_atel_num(20000)
        self.assertEqual(db.get_next_atel_num(),20000)

        db.set_next_atel_num(old_num)

    def testLastUpdatedDate(self):
        #set up
        old_date = db.get_last_updated_date()

        _set_last_updated_date(datetime(2021,8,16))
        self.assertEqual(db.get_last_updated_date(),datetime(2021, 8, 16))

        _set_last_updated_date(old_date)

    def testReports(self):
        report = ImportedReport(20000,"db_test_report","A","B",datetime(2021,8,12), keywords=["star","radio"])

        db.add_report(report)
        try:
            results = db.find_reports_by_object(SearchFilters(term="db_test_report"))
            result = results[0]

            self.assertEqual(report,result)
            self.assertTrue(db.report_exists(20000))
        finally:
            #delete report
            cn = db._connect()
            cur:MySQLCursor = cn.cursor()
            cur.execute("delete from Reports where atelNum = 20000")
            cur.close()
            cn.commit()
            cn.close()

    def testBuildBaseQuery(self):
        self.assertEqual(db._build_report_base_query(), "select atelNum, title, authors, body, submissionDate from Reports ")

    def testBuildWhereClause(self):
        #Test full query
        sf = SearchFilters("term",["star","planet"],KeywordMode.ANY)
        df = DateFilter(datetime(2021, 8, 16), datetime(2021, 8, 17))
        query, data = db._build_where_clause(sf,df)
        self.maxDiff = None
        self.assertEqual(query, "where submissionDate >= %s and submissionDate <= %s and (title like concat('%', %s, '%') or body like concat('%', %s, '%')) and (FIND_IN_SET(%s, keywords) > 0 or FIND_IN_SET(%s, keywords) > 0) ")
        self.assertTupleEqual(data,(df.start_date,df.end_date,sf.term,sf.term,sf.keywords[0],sf.keywords[1]))

        #Test keyword modes / single filter
        sf2 = SearchFilters(term=None, keywords=["star","planet"], keyword_mode=KeywordMode.ALL)
        query2, data2 = db._build_where_clause(sf2)
        self.assertEqual(query2,"where (FIND_IN_SET(%s, keywords) > 0 and FIND_IN_SET(%s, keywords) > 0) ")
        self.assertTupleEqual(data2,(sf.keywords[0],sf.keywords[1]))

        sf2.keyword_mode = KeywordMode.NONE
        query3, data3 = db._build_where_clause(sf2)
        self.assertEqual(query3,"where (FIND_IN_SET(%s, keywords) = 0 and FIND_IN_SET(%s, keywords) = 0) ")
        self.assertTupleEqual(data3,(sf.keywords[0],sf.keywords[1]))

        #Test empty query
        sf = None
        query, data = db._build_where_clause(sf)
        self.maxDiff = None
        self.assertEqual(query,"")
        self.assertTupleEqual(data,())

    def testFindGeneric(self):
        report = ImportedReport(20001,"db_test_report","db_test_authors_text","db_test_body_text", datetime(2021,8,12), keywords=["star","radio"])

        db.add_report(report)
        try:
            #test search body
            results = db.find_reports_by_object(SearchFilters(term="db_test_b"))
            result = results[0]
            self.assertEqual(report,result)

            #test search title
            results = db.find_reports_by_object(SearchFilters(term="db_test_report"))
            result = results[0]
            self.assertEqual(report,result)

            #Test search author (not possible)
            results = db.find_reports_by_object(SearchFilters(term="db_test_authors"))
            self.assertListEqual(results,[])

            #Test start date
            results = db.find_reports_by_object(SearchFilters(term="db_test_b"), DateFilter(start_date=datetime(2021,8,11)))
            result = results[0]
            self.assertEqual(report,result)

            #Test end date
            results = db.find_reports_by_object(SearchFilters(term="db_test_b"), DateFilter(end_date=datetime(2021,8,13)))
            result = results[0]
            self.assertEqual(report,result)

            #Test keywords - all
            results = db.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","radio"],keyword_mode=KeywordMode.ALL))
            result = results[0]
            self.assertEqual(report,result)

            results = db.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","planet"],keyword_mode=KeywordMode.ALL))
            self.assertListEqual(results,[])

            #Test keywords - any
            results = db.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","radio"],keyword_mode=KeywordMode.ANY))
            result = results[0]
            self.assertEqual(report,result)

            results = db.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","planet"],keyword_mode=KeywordMode.ANY))
            result = results[0]
            self.assertEqual(report,result)

            #Test keywords - none
            results = db.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star", "radio"], keyword_mode=KeywordMode.NONE))
            self.assertListEqual(results,[])

            results = db.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","planet"],keyword_mode=KeywordMode.NONE))
            self.assertListEqual(results,[])

            results = db.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["nova","planet"],keyword_mode=KeywordMode.NONE))
            result = results[0]
            self.assertEqual(report, result)

            #Test composite
            results = db.find_reports_by_object(
                SearchFilters(
                    term="B", 
                    keywords=["star","radio"], 
                    keyword_mode=KeywordMode.ALL),
                DateFilter(
                    start_date=datetime(2021,8,11), 
                    end_date=datetime(2021,8,13)
                )
            )
            result = results[0]
            self.assertIn(report, results)

            #Test no filters
            result = db.find_reports_by_object(
                object_name=""
            )
            self.assertListEqual(result,[])

        finally:
            #delete report
            cn = db._connect()
            cur:MySQLCursor = cn.cursor()
            cur.execute("delete from Reports where atelNum = 20001")
            cur.close()
            cn.commit()
            cn.close()

class TestObjects(unittest.TestCase):
    def setUp(self):
        # clean up test objects and aliases if already exists
        cn = db._connect()
        cur = cn.cursor()
        cur.execute("delete from Objects where objectID like 'test_main_id'")
        cn.commit()
        cur.close()
        cn.close()

        # add test object
        self.ex_coords = SkyCoord("13h36m50s", "30d20m20s", frame="icrs", unit=("hourangle", "deg"))
        db.add_object("test_main_id", self.ex_coords, ["test-alias-1", "test-alias-2"])

    def testAddObject(self):
        cn = db._connect()
        cur:MySQLCursor = cn.cursor()
        
        cur.execute("select * from Objects where objectID like 'test_main_id'")
        result = cur.fetchone()
        self.assertEqual(result[0], "test_main_id")
        self.assertAlmostEqual(float(result[1]), self.ex_coords.ra.hourangle.item(),10)
        self.assertAlmostEqual(float(result[2]), self.ex_coords.dec.deg.item(),10)

        cur.execute("select * from Aliases where objectIDFK like 'test_main_id'")
        results = cur.fetchall()
        self.assertIsNotNone(results)
        result1 = results[0]
        result2 = results[1]
        self.assertEqual(result1[0],"test-alias-1")
        self.assertEqual(result1[1], "test_main_id")
        self.assertEqual(result2[0], "test-alias-2")
        self.assertEqual(result2[1], "test_main_id")

        cn.commit()
        cur.close()
        cn.close()

    def testInvalidObject(self):
        with self.assertRaises(db.ExistingObjectError):
            db.add_object("test_main_id", self.ex_coords , ["test-alias-1", "test-alias-2"])
        with self.assertRaises(ValueError):
            db.add_object("A"*257, self.ex_coords, [])

    def testAddAliases(self):
        db.add_aliases("test_main_id",["test-alias-3","test-alias-4"])

        cn = db._connect()
        cur: MySQLCursor = cn.cursor()
        cur.execute("select * from Aliases where objectIDFK like 'test_main_id'")
        results = cur.fetchall()
        self.assertIsNotNone(results)
        result1 = results[2]
        result2 = results[3]
        self.assertEqual(result1[0], "test-alias-3")
        self.assertEqual(result1[1], "test_main_id")
        self.assertEqual(result2[0], "test-alias-4")
        self.assertEqual(result2[1], "test_main_id")
        cn.commit()
        cur.close()
        cn.close()

        with self.assertRaises(db.ObjectNotFoundError):
            db.add_aliases("test-invalid-id",["test-alias"])

    def testGetAllAliases(self):
        results = db.get_all_aliases()
        self.assertCountEqual(results,[AliasResult("test-alias-1","test_main_id"),AliasResult("test-alias-2","test_main_id")])

    def testObjectExists(self):
        #check valid
        exists, lastUpdated = db.object_exists("test-alias-1")
        self.assertTrue(exists)
        self.assertTrue(type(lastUpdated)==datetime)
        exists, lastUpdated = db.object_exists("test_main_id")
        self.assertTrue(exists)
        self.assertTrue(type(lastUpdated)==datetime)
        #check invalid
        exists, lastUpdated = db.object_exists("test_other_alias")
        self.assertFalse(exists)
        self.assertIsNone(lastUpdated)

    def testGetObjectID(self):
        self.assertEqual(db._get_object_id("test-alIas-1"),"test_main_id")
        self.assertEqual(db._get_object_id("test-AlIas-2"), "test_main_id")
        self.assertEqual(db._get_object_id("test_main_ID"), "test_main_id")

        with self.assertRaises(db.ObjectNotFoundError):
            db._get_object_id("test-other-alias")

    def testGetObjectCoords(self):
        coords = db.get_object_coords("test-alias-1")
        self.assertAlmostEqual(coords.ra.hourangle.item(), self.ex_coords.ra.hourangle.item())
        self.assertAlmostEqual(coords.dec.deg.item(), self.ex_coords.dec.deg.item())

        with self.assertRaises(db.ObjectNotFoundError):
            db.get_object_coords("test-other-alias")

    def testLinkReports(self):
        #Test case - alias in title
        db.add_report(ImportedReport(99999, "test-db-title-about:test-alias-1, findings","db-test-authors","db-test-body",datetime(2021,9,18)))
        #Test case - main id in title
        db.add_report(ImportedReport(99998, "test-db-title-about:Test_main_id, findings","db-test-authors","db-test-body",datetime(2021,9,18)))
        #Test case - alias in body
        db.add_report(ImportedReport(99997, "test-db-title, findings","db-test-authors","db-test-body-test-Alias-2",datetime(2021,9,18)))
        #Test case - main id in body
        db.add_report(ImportedReport(99996, "test-db-title, findings", "db-test-authors", "test_main_iddb-test-body", datetime(2021, 9, 18)))
        #Test case - no matches in body or title
        db.add_report(ImportedReport(99995, "test-db-title, findings", "db-test-authors-test-alias-1", "db-test-body", datetime(2021, 9, 18)))

        # call function
        db._link_reports("test_main_id",["test-alias-1","test-alias-2"])

        # check results from db
        cn = db._connect()
        cur: MySQLCursor = cn.cursor()
        cur.execute("select * from ObjectRefs")
        results = cur.fetchall()

        self.assertIn((99999,"test_main_id"),results)
        self.assertIn((99998,"test_main_id"),results)
        self.assertIn((99997,"test_main_id"),results)
        self.assertIn((99996,"test_main_id"),results)
        self.assertNotIn((99995,"test_main_id"),results)

        # ensure it ignores duplicate entries
        db._link_reports("test_main_id", ["test-alias-1", "test-alias-2"])

        # clean up
        cur.execute("delete from Reports where atelNum between 99995 and 99999")
        cn.commit()
        cur.close()
        cn.close()

    def testBuildJoinClause(self):
        #using main id
        query, data = db._build_join_clause("test_main_id") 
        self.assertEqual(query, "right join ObjectRefs on Reports.atelNum = ObjectRefs.atelNumFK and ObjectRefs.objectIDFK = %s ")
        self.assertTupleEqual(data, ("test_main_id",))

        # using alias
        query, data = db._build_join_clause("test-alias-1")
        self.assertEqual(query, "right join ObjectRefs on Reports.atelNum = ObjectRefs.atelNumFK and ObjectRefs.objectIDFK = %s ")
        self.assertTupleEqual(data, ("test_main_id",))
        
        # using none
        query, data = db._build_join_clause(None)
        self.assertEqual(query, "")
        self.assertTupleEqual(data, ())

        # using invalid alias
        with self.assertRaises(db.ObjectNotFoundError):
            db._build_join_clause("db-test-invalid-alias")

    def testBuildReportNameQuery(self):
        self.maxDiff = None

        sf=SearchFilters("term", ["star", "planet"], KeywordMode.ANY)
        df=DateFilter(datetime(2021, 8, 16), datetime(2021, 8, 17))

        # Test empty query
        query, data = db._build_report_name_query()
        self.assertEqual(query,"select atelNum, title, authors, body, submissionDate from Reports ")
        self.assertTupleEqual(data, ())

        # Test only object name
        query, data = db._build_report_name_query(object_name="test-alias-1")
        self.assertEqual(query, "select atelNum, title, authors, body, submissionDate from Reports right join ObjectRefs on Reports.atelNum = ObjectRefs.atelNumFK and ObjectRefs.objectIDFK = %s ")
        self.assertTupleEqual(data, ("test_main_id",))

        # Test only filters
        query, data = db._build_report_name_query(sf,df)
        self.assertEqual(query, "select atelNum, title, authors, body, submissionDate from Reports where submissionDate >= %s and submissionDate <= %s and (title like concat('%', %s, '%') or body like concat('%', %s, '%')) and (FIND_IN_SET(%s, keywords) > 0 or FIND_IN_SET(%s, keywords) > 0) ")
        self.assertTupleEqual(data, (df.start_date, df.end_date, sf.term, sf.term, sf.keywords[0], sf.keywords[1]))

        # Test full query
        query, data = db._build_report_name_query(sf,df,"test_main_id")
        self.assertEqual(query, "select atelNum, title, authors, body, submissionDate from Reports right join ObjectRefs on Reports.atelNum = ObjectRefs.atelNumFK and ObjectRefs.objectIDFK = %s where submissionDate >= %s and submissionDate <= %s and (title like concat('%', %s, '%') or body like concat('%', %s, '%')) and (FIND_IN_SET(%s, keywords) > 0 or FIND_IN_SET(%s, keywords) > 0) ")
        self.assertTupleEqual(data, ("test_main_id", df.start_date, df.end_date, sf.term, sf.term, sf.keywords[0], sf.keywords[1]))

    def testFindByObject(self):
        report = ImportedReport(20001, "db_test_report", "db_test_authors_text","db_test_body_text", datetime(2021, 8, 12), keywords=["star", "radio"], objects=["test_main_id"])
        report2 = ImportedReport(20000, "db_test_report", "db_test_authors_text", "db_test_body_text", datetime(2021, 8, 12), keywords=["star", "radio"])

        db.add_report(report2)
        db.add_report(report)

        try:
            #test search main id
            results = db.find_reports_by_object(object_name="test_main_id")
            result = results[0]
            self.assertEqual(report, result)

            #test search alias
            results = db.find_reports_by_object(object_name="test-alias-1")
            result = results[0]
            self.assertEqual(report, result)

            #test search invalid object
            results = db.find_reports_by_object(object_name="test-alias-3")
            self.assertEqual(results, [])

            #test full query
            results = db.find_reports_by_object(
                SearchFilters(
                    term="B",
                    keywords=["star", "radio"],
                    keyword_mode=KeywordMode.ALL),
                DateFilter(
                    start_date=datetime(2021, 8, 11),
                    end_date=datetime(2021, 8, 13)
                ),
                object_name="test_main_id")
            result = results[0]
            self.assertEqual(report, result)

            #test full query - invalid object
            results = db.find_reports_by_object(
                SearchFilters(
                    term="B",
                    keywords=["star", "radio"],
                    keyword_mode=KeywordMode.ALL),
                DateFilter(
                    start_date=datetime(2021, 8, 11),
                    end_date=datetime(2021, 8, 13)
                ),
                object_name="test-alias-3")
            self.assertEqual(results,[])

        finally:
            #delete report
            cn = db._connect()
            cur: MySQLCursor = cn.cursor()
            cur.execute("delete from Reports where atelNum = 20001 or atelNum = 20000")
            cur.close()
            cn.commit()
            cn.close()

    def tearDown(self):
        cn = db._connect()
        cur:MySQLCursor = cn.cursor()

        # clean up test objects and aliases
        cur.execute("delete from Objects where objectID like 'test_main_id'")        

        cn.commit()
        cur.close()
        cn.close()
        
        

# Helper methods
def _set_last_updated_date(date: datetime):
    """
    Sets the date that the database was updated with the latest ATel reports.
    For testing purposes only, in production this should only be set to CURDATE() by add_report().

    Args:
        date (datetime): The date that the database was updated with the latest ATel reports.
    """
    cn = db._connect()
    cur:MySQLCursor = cn.cursor()

    query = ("update Metadata "
             "set lastUpdatedDate = %s")

    try:
        cur.execute(query, (date,))
    except mysql.connector.Error as e:
        raise e
    finally:
        cn.commit()
        cur.close()
        cn.close()

if __name__ == '__main__':
    unittest.main()
