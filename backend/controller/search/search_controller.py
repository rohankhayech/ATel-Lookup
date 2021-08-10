""" The search controller is used to help with the actual searching aspect of our system.

Author:
    Tully Slattery

License Terms and Copyright:
    Copyright (C) 2021 Tully Slattery

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

import json
from typing import Tuple


def search(json: json) -> Tuple[bool, list[reports_list], list[nodes_list], list[edges_list]]:
    '''The purpose of this function is to help with the actual searching aspect of our system, 
    it will be called by the submit search form, and will call the either of the search functions 
    in the search module, as well as both visualisation functions. 

    Args:
        json (json): a JSON object containing relevant fields. See SAS for breakdown of fields.
    
    Returns:
        bool: determines whether the search was successful.
        reports_list: a list of ATel reports returned by search queries. 
        nodes_list: a list of report nodes for the visualisation graph. 
        edges_list: a list of edges for the visualisation graph.  

    '''
    return True, [], [], [] #stub