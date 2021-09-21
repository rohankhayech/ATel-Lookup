""" Unit testing for view.vis

Author:
    Ryan Martin

License Terms and Copyright:
    Copyright (C) 2021 Ryan Martin

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
import unittest as ut
import random as r
import string 

from view import vis 
from model.ds.report_types import ReportResult


def gen_reports(num_reports: int, related: bool) -> tuple[list[int], list[ReportResult]]:
    if num_reports < 5:
        raise ValueError('Num reports must be >= 5')

    atel_numbers = []
    reports = [] 

    # Random ATel numbers
    for _ in range(num_reports):
        atel_numbers.append(r.randint(0, 15000))
    
    for num in atel_numbers:
        ref_reports = [] 
        if related:
            for _ in range(1, r.randint(0, len(atel_numbers) - 2)):
                rand = -1 
                while rand == -1 or rand in ref_reports or rand == num:
                    rand = atel_numbers[r.randint(0, len(atel_numbers) - 1)]
                ref_reports.append(rand)

        reports.append(ReportResult(
            num, 
            ''.join(r.choices(string.ascii_uppercase)), 
            "", 
            "",
            datetime(2000, 1, 1), 
            ref_reports
        ))

    return atel_numbers, reports 


class TestVis(ut.TestCase):
    def setUp(self) -> None:
        self.related_atel_pool, self.reports_related = gen_reports(50, True)
        self.unrelated_atel_pool, self.reports_unrelated = gen_reports(50, False) 


    def test_unrelated(self):
        '''
        Case 1: If there are no related reports, we don't expect no nodes to be created. 
        (No graph)
        '''
        nodes_result, edges_result = vis.create_nodes_list(self.reports_unrelated)
        self.assertFalse(len(self.reports_unrelated) == 0)
        self.assertEqual(nodes_result, [])
        self.assertEqual(edges_result, [])
        self.assertTrue(len(nodes_result) + len(edges_result) == 0)


    def test_related(self):
        '''
        Case 2: Reports are related and nodes are constructed. 
        '''
        nodes_result, edges_result = vis.create_nodes_list(self.reports_related)
        self.assertFalse(len(self.reports_unrelated) == 0)
        self.assertNotEqual(nodes_result, [])
        self.assertNotEqual(edges_result, [])
        for edge in edges_result:
            self.assertTrue(edge[0] in self.related_atel_pool)
            self.assertTrue(edge[1] in self.related_atel_pool)
            

if __name__ == '__main__':
    ut.main()