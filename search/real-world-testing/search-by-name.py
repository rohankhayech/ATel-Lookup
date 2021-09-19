#
# Real world testing: Search Module.
# Part 1: Search by name. 
#
# This script works as a utility rather than a unit test. Use this to retrieve results from 
# the external search module, and manually compare them with expected results. 
# A report is accompanied with this script.
#
# Author: Ryan Martin.
#


import sys
import search.query_simbad as qs


def usage():
    print(
        """
        Search Module Utility: Search by name/ID. 
        Usage:
        =========================================
        python search-by-name.py [id/name] [-a (optional)]

        [id/name] -> The string identifier or name of the object. 
        [-a]      -> Use this option to retrieve aliases too. Otherwise, only 
                    the MAIN_ID will be retrieved. 
        """
    )


def retrieve(name: str, get_aliases: bool):
    name, coords, aliases = qs.query_simbad_by_name(name, False)
    print(
        " MAIN_ID:", name, "\n", 
        "RA:     ", coords.ra.hms, "\n", 
        "DEC:    ", coords.dec.dms, "\n", 
        "aliases:", aliases
    )


def main(argv: list[str]):
    get_aliases = False 

    if len(argv) not in [2, 3]:
        usage() 
    else:
        name = argv[1] 
        if len(argv) == 3:
            if argv[2] == '-a':
                get_aliases = True 
            else:
                usage() 
        retrieve(name, get_aliases)


if __name__ == '__main__':
    main(sys.argv) 