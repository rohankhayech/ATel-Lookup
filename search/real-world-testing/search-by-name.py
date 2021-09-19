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


import search.query_simbad as qs


def retrieve(name: str, get_aliases: bool):
    name, coords, aliases = qs.query_simbad_by_name(name, get_aliases)
    print(
        " MAIN_ID:", name, "\n", 
        "RA:     ", coords.ra.hms, "\n", 
        "DEC:    ", coords.dec.dms, "\n", 
        "NumAls: ", len(aliases),
        "aliases:", aliases
    )


def main():
    while (True):
        name = input('Enter name:') 
        retrieve(name, True)


if __name__ == '__main__':
    main() 