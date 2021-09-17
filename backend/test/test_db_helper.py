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
from model.ds.search_filters import KeywordMode
from datetime import datetime
import unittest

from mysql.connector.cursor import MySQLCursor
import mysql.connector

from model.db import db_interface
from model.ds.report_types import ImportedReport
from model.ds.search_filters import SearchFilters

class TestInitTables(unittest.TestCase):
    #Verify tables exist/were created on container init
    def testTables(self):
        _verifyTable(self,"AdminUsers")
        _verifyTable(self, "Reports")
        _verifyTable(self,"Metadata")

def _verifyTable(self, table_name):
    cn = db_interface._connect()
    cur:MySQLCursor = cn.cursor()

    cur.execute(f"show tables like '{table_name}'")

    result = cur.fetchone()

    cur.close()
    cn.close()

    self.assertTrue(result)

class TestAuth(unittest.TestCase):
    
    def testAddUser(self):
        db_interface.add_admin_user("test","hash")
        self.assertTrue(db_interface.user_exists("test"))
    
    def testDupeUser(self):
        db_interface.add_admin_user("test", "hash")
        with (self.assertRaises(db_interface.ExistingUserError)):
            db_interface.add_admin_user("test","hash")

    def testUserNotExists(self):
        self.assertFalse(db_interface.user_exists("test2"))

    def testGetPassword(self):
        db_interface.add_admin_user("test", "hash")
        self.assertEqual(db_interface.get_hashed_password("test"),"hash")
        with (self.assertRaises(db_interface.UserNotFoundError)):
            db_interface.get_hashed_password("test2")

    def testExceedsMax(self):
        with (self.assertRaises(ValueError)):
            db_interface.add_admin_user("a"*26,"hash")
        with (self.assertRaises(ValueError)):
            db_interface.add_admin_user("test","a"*256)
        with (self.assertRaises(ValueError)):
            db_interface.add_admin_user("","hash")
        with (self.assertRaises(ValueError)):
            db_interface.add_admin_user("test","")

    def tearDown(self):
        #remove test user
        cn = db_interface._connect()
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
        old_num = db_interface.get_next_atel_num()

        db_interface.set_next_atel_num(20000)
        self.assertEqual(db_interface.get_next_atel_num(),20000)

        db_interface.set_next_atel_num(old_num)

    def testLastUpdatedDate(self):
        #set up
        old_date = db_interface.get_last_updated_date()

        _set_last_updated_date(datetime(2021,8,16))
        self.assertEqual(db_interface.get_last_updated_date(),datetime(2021, 8, 16))

        _set_last_updated_date(old_date)

    def testReports(self):
        report = ImportedReport(20000,"db_test_report","A","B",datetime(2021,8,12), keywords=["star","radio"])

        db_interface.add_report(report)
        try:
            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_report"))
            result = results[0]

            self.assertEqual(report,result)
            self.assertTrue(db_interface.report_exists(20000))
        finally:
            #delete report
            cn = db_interface._connect()
            cur:MySQLCursor = cn.cursor()
            cur.execute("delete from Reports where atelNum = 20000")
            cur.close()
            cn.commit()
            cn.close()

    def testBuildQuery(self):
        #Test full query
        sf = SearchFilters("term",["star","planet"],KeywordMode.ANY,datetime(2021,8,16),datetime(2021,8,17))
        query, data = db_interface._build_report_query(sf)
        self.maxDiff = None
        self.assertEqual(query,"select atelNum, title, authors, body, submissionDate from Reports where (title like concat('%', %s, '%') or body like concat('%', %s, '%')) and submissionDate >= %s and submissionDate <= %s and (FIND_IN_SET(%s, keywords) > 0 or FIND_IN_SET(%s, keywords) > 0) ")
        self.assertTupleEqual(data,(sf.term,sf.term,sf.start_date,sf.end_date,sf.keywords[0],sf.keywords[1]))

        #Test keyword modes / single filter
        sf2 = SearchFilters(term=None, keywords=["star","planet"], keyword_mode=KeywordMode.ALL)
        query2, data2 = db_interface._build_report_query(sf2)
        self.assertEqual(query2,"select atelNum, title, authors, body, submissionDate from Reports where (FIND_IN_SET(%s, keywords) > 0 and FIND_IN_SET(%s, keywords) > 0) ")
        self.assertTupleEqual(data2,(sf.keywords[0],sf.keywords[1]))

        sf2.keyword_mode = KeywordMode.NONE
        query3, data3 = db_interface._build_report_query(sf2)
        self.assertEqual(query3,"select atelNum, title, authors, body, submissionDate from Reports where (FIND_IN_SET(%s, keywords) = 0 and FIND_IN_SET(%s, keywords) = 0) ")
        self.assertTupleEqual(data3,(sf.keywords[0],sf.keywords[1]))

        #Test empty query
        sf = None
        query, data = db_interface._build_report_query(sf)
        self.maxDiff = None
        self.assertEqual(query,"select atelNum, title, authors, body, submissionDate from Reports where ")
        self.assertTupleEqual(data,())

    def testFindGeneric(self):
        report = ImportedReport(20001,"db_test_report","db_test_authors_text","db_test_body_text", datetime(2021,8,12), keywords=["star","radio"])

        db_interface.add_report(report)
        try:
            #test search body
            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b"))
            result = results[0]
            self.assertEqual(report,result)

            #test search title
            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_report"))
            result = results[0]
            self.assertEqual(report,result)

            #Test search author (not possible)
            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_authors"))
            self.assertListEqual(results,[])

            #Test start date
            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b", start_date=datetime(2021,8,11)))
            result = results[0]
            self.assertEqual(report,result)

            #Test end date
            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b", end_date=datetime(2021,8,13)))
            result = results[0]
            self.assertEqual(report,result)

            #Test keywords - all
            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","radio"],keyword_mode=KeywordMode.ALL))
            result = results[0]
            self.assertEqual(report,result)

            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","planet"],keyword_mode=KeywordMode.ALL))
            self.assertListEqual(results,[])

            #Test keywords - any
            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","radio"],keyword_mode=KeywordMode.ANY))
            result = results[0]
            self.assertEqual(report,result)

            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","planet"],keyword_mode=KeywordMode.ANY))
            result = results[0]
            self.assertEqual(report,result)

            #Test keywords - none
            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star", "radio"], keyword_mode=KeywordMode.NONE))
            self.assertListEqual(results,[])

            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["star","planet"],keyword_mode=KeywordMode.NONE))
            self.assertListEqual(results,[])

            results = db_interface.find_reports_by_object(SearchFilters(term="db_test_b", keywords=["nova","planet"],keyword_mode=KeywordMode.NONE))
            result = results[0]
            self.assertEqual(report, result)

            #Test composite
            results = db_interface.find_reports_by_object(
                SearchFilters(
                    term="B", 
                    keywords=["star","radio"], 
                    keyword_mode=KeywordMode.ALL, 
                    start_date=datetime(2021,8,11), 
                    end_date=datetime(2021,8,13)
                )
            )
            result = results[0]
            self.assertEqual(report, result)

            #Test no filters
            result = db_interface.find_reports_by_object(
                object_name=""
            )
            self.assertListEqual(result,[])

        finally:
            #delete report
            cn = db_interface._connect()
            cur:MySQLCursor = cn.cursor()
            cur.execute("delete from Reports where atelNum = 20001")
            cur.close()
            cn.commit()
            cn.close()


# Helper methods
def _set_last_updated_date(date: datetime):
    """
    Sets the date that the database was updated with the latest ATel reports.
    For testing purposes only, in production this should only be set to CURDATE() by add_report().

    Args:
        date (datetime): The date that the database was updated with the latest ATel reports.
    """
    cn = db_interface._connect()
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
