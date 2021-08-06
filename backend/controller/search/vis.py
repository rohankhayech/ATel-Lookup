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
        reports_list (List[ReportResult]): A list of ReportResult objects
        returned from a successful search. 

    Returns:
        ReportsList: the nodes list for the graph. The list
            contains a tuple representing an integer for the ATel number and a 
            datetime field for the report's observation date. 
        EdgesList: the edge list. An edge is represented by a pair
            of ATel numbers. 
    '''
    return [], [] # Stub