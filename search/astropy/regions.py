from astroquery.simbad import Simbad 
from astropy.coordinates import SkyCoord 

# Return a list of object ids that match the region.
def get_objects_in_region(coords, radius):
    if not isinstance(coords, SkyCoord):
        return None 
    else:
        formatted_radius = radius + ' deg' 
        result = Simbad.query_region(coords, formatted_radius) 
        if not result:
            return None 
        else:
            lst = [] 
            for line in str(result['MAIN_ID']).splitlines():
                value = line.strip()
                if value != 'MAIN_ID' and not value.startswith('--'):
                    lst.append(value)
            return lst 

# Sample coordinates provided by client for demonstration:
coords = SkyCoord('18h20m21.9424s', '7d11m07.278s')
radius = '0.1'

print(get_objects_in_region(coords, radius) )