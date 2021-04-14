from astropy import units as u 
from astropy.coordinates import Angle, SkyCoord

# Demonstrates converting between units (decimal degrees/HMS/DMS) and 
# coordinate systems (ICRS/galactic)
#
# Author: Ryan Martin

####################
# Converting units #
####################

print ('\nPart 1: Unit conversions\n')

hms = Angle('00h23m40s') # hms sexagesimal notation 
print (hms, 'to degrees:', hms.deg) # convert to degrees

dms = Angle('23d47m03s') # decimal degrees, arcminutes, arcseconds sexagesimal
print (dms, 'to degrees:', dms.deg) # convert to degrees

dec = Angle('7.5929492d') # decimal degrees 
print (dec.deg, 'to sexagesimal hms:', dec.hms) # convert to sexagesimal notation (hms) 
print (dec.deg, 'to sexagesimal dms:', dec.dms) # convert to sexagesimal notation (dms) 

######################
# Converting systems #
######################

print ('\nPart 2: System conversions\n')

galactic = SkyCoord(frame='galactic', l='13.21d', b='62.14d')
print ('Galactic example:', galactic)

# Convert this from galactic to ICRS:
print ('Converted to ICRS:', galactic.icrs)