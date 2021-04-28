#
# This script combines searching by object coordinates and finding
# aliases for the objects. This is equivalent to Functional Requirement
# 8. 
#
# Author:     Ryan Martin
# Created:    28/04/2021
#

import re

from astropy.coordinates import SkyCoord 
from astroquery.simbad import Simbad

import astropy.units as u

#
# This function creates an astropy.SkyCoord object from a set of 
# ICRS coordinates. The function checks if the input ends in 's' 
# for each value and assumes it's in sexagesimal notation. Otherwise,
# the function will assume it is a float and will try to convert
# the string to a float. The units must be specified if the coordinates
# are not in sexagesimal notation, hence the need for a units vector. 
# 
# Returns:  sky_coord, the SkyCoord object. 
# Raises:   ValueError if not a float or sexagesimal (assumed).
#           UnitsError if the units cannot be determined. 
#
def get_sky_coord(ra, dec, rad):
    sky_coord = None

    # Any invalid input is handled by the UnitsError. 
    # Regex matching could be considered here, but may not be necessary. 
    coords = [ra, dec, rad]
    units = [None] * 3

    for i in range(0, 2):
        if not coords[i].endswith('s'):
            try:
                coords[i] = float(coords[i])
                units[i] = u.deg
            except ValueError:
                print('Coordinates are not float or sexagesimal.')
                raise 

    try:
        sky_coord = SkyCoord(ra, dec, frame = 'icrs', unit=units)
    except u.UnitsError as err:
        # This exception is raised when the SkyCoord constructor
        # cannot identify the units provided. 
        # This should be an error displayed via front-end.
        print('Coordinates were entered in an invalid format. ', err)
        raise

    return sky_coord

# This function is from the regions.py file.
# Modified to remove radius. 
# See: prototypes -> search/astropy/regions.py
def get_objects_in_region(coords):
    lst = []
    if isinstance(coords, SkyCoord):
        result = Simbad.query_region(coords) 
        if result:
            for line in str(result['MAIN_ID']).splitlines():
                value = line.strip()
                if value != 'MAIN_ID' and not value.startswith('--'):
                    lst.append(value)
            return lst 
    return lst 

def get_alias(id):
    # Query SIMBAD
    result = Simbad.query_objectids(id) 
    if (result == None):
        # Object not found.
        return [] 
    else:
        lst = []
        for line in str(result).splitlines(): 
            value = line.strip() 
            # Ignore table heading.
            if value != 'ID' and not value.startswith('--'):
                lst.append(value)
        return lst 

def get_aliases(ids):
    aliases = [] 
    for i in ids:
        try:
            lst = get_alias(i)
            for j in lst:
                aliases.append(j)
        except TypeError:
            pass 
    return aliases
#
# Main function, emulating a coordinate search. 
# Values to try:
#
#   RA:     2.3     1h2m3s
#   DEC:    2.3     2d3m4s
#   rad:    0.2     0.2
#
def main():

    # All values must be either in decimal degrees or sexagesimal. 
    ra = input('Enter RA coordinate: ')
    dec = input('Enter DEC coordinate: ') 
    rad = input('Enter radius: ')

    # Raises ValueError if failed to convert to float. 
    coords = get_sky_coord(ra, dec, rad)

    # Get the objects in region specified in coordinates.
    objects_in_region = get_objects_in_region(coords)
    # Get the aliases for each object in the region. 
    object_aliases_in_region = get_aliases(objects_in_region)

    # For demonstration purposes, print the results. 
    # Note: There seems to be a bug in astropy where a FutureWarning is raised
    # when comparing elements. This does not crash the program, it's a warning.
    # Something to do with the internal code... 
    print (object_aliases_in_region)

if __name__ == "__main__":
    main() 