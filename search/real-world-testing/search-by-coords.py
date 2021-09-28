#
# Real world testing: Search Module.
# Part 2: Search by coordinates. 
#
# This script works as a utility rather than a unit test. Use this to retrieve results from 
# the external search module, and manually compare them with expected results. 
# A report is accompanied with this script.
#
# Author: Ryan Martin.
# 


from astropy.coordinates.sky_coordinate import SkyCoord
import search.query_simbad as qs


def retrieve(ra: str, dec: str):
    s = SkyCoord(ra, dec, frame='icrs', unit=('hourangle', 'deg'))
    result = qs.query_simbad_by_coords(s) 
    print(result)


def main():
    while (True):
        ra = input('Enter RA: ') 
        dec = input('Enter DEC: ') 
        retrieve(ra, dec)


if __name__ == '__main__':
    main() 