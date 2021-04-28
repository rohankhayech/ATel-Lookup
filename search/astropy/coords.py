from astropy.coordinates import SkyCoord 
from astropy import units as u 

# Demonstrating the representation of astronomical
# coordinates using astropy.coordinates.SkyCoord. 
#
# Author: Ryan Martin 
# Date: 13.04.2021

# Example 1: A coordinate that uses the standard
# sexagesimal notation (hms/dms)

example = SkyCoord('00h23m40s','+19d33m27s')
print('Example 1: ', example) 

# Example 2: The same as example 1, however for 
# RA and DEC, use decimal degrees. 

example_2 = SkyCoord('5.91666667','19.5575', unit='deg')
print('Example 2: ', example_2) 

# Example 3: A galactic coordinate, longitude 
# and latitude in decimal degrees.

example_3 = SkyCoord(frame='galactic', l='13.23', b='42.42', unit='deg')
print('Example 3: ', example_3)