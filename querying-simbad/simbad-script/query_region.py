from astroquery.simbad import Simbad 
from astropy.coordinates import SkyCoord 

# RA = Right ascension, hour angle. 
coords_ra   = '18 20 21.9424'

# DEC = Declination, decimal degrees. 
coords_dec  = '+07 11 07.278'

# Radius, degrees.
rad         = '0.1' 

# Create the SkyCoord object 
# Specify the frame and units of the input. 
coords = SkyCoord(coords_ra, coords_dec, frame = 'icrs', unit = ('hourangle', 'deg'))

result = Simbad.query_region(coords, radius = rad + ' deg')
print(result['MAIN_ID'][0])