""" The visualisations module is responsible for processing data and constructing
    representations of this data into an appropriate format for graphical 
    display. 

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


# Type aliasing for the list data structures. 
ReportsList = list[tuple[int, datetime]]
EdgesList = list[tuple[int, int]]


def create_nodes_list(reports_list: list[ReportResult]
) -> tuple[ReportsList, EdgesList]:
    ''' Constructs the data structures required to graph relations between
        ATel reports. The data is structured like a standard graph, involving
        a list of nodes and edges. Reports are considered related by their 
        referenced reports (a field that is included in the ReportResult
        data type).

    Args:
        reports_list (list[ReportResult]): A list of ReportResult objects
        returned from a successful search. 

    Returns:
        ReportsList: the nodes list for the graph. The list
            contains a tuple representing an integer for the ATel number and a 
            datetime field for the report's observation date. 
        EdgesList: the edge list. An edge is represented by a pair
            of ATel numbers. 
    '''
    return [], [] # Stub