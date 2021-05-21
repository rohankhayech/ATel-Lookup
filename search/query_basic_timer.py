import time
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
from astropy.units import Unit as u

#
# This script is the most basic level of scheduling SIMBAD queries. It does not implement a 
# task queue, but rather a basic timer based on UNIX epoch time. The script will check to see
# if enough time has elapsed before querying SIMBAD, as defined by the DELAY_INTERVAL constant, 
# which is currently 0.2 seconds. 
#
# This is not a totally thread-safe program, nor is it generally good programming practice. 
# It implements the concept, and should be used as a reference only. 
#

# The delay
DELAY_INTERVAL = 0.2

# Test data
TEST_NAMES = ['m13', 'm1', 'm4', 'm5', 'm3', 'm3']


class SimbadQuery:
    def __init__(self):
        pass 


class NameQuery(SimbadQuery):
    def __init__(self, id: str):
        self.id = id 


class CoordsQuery(SimbadQuery):
    def __init__(self, coords: SkyCoord, radius=20):
        self.coords = coords 
        self.radius = radius 


class QuerySimbad:
    def __init__(self, debug=False):
        self._epoch = time.time() 
        self.DEBUG = debug

    # There is probably a much more thread-safe way of achieving this. 
    def _begin(self):
        if self.DEBUG: print ('Waiting...')
        while time.time() - self._epoch < DELAY_INTERVAL:
            pass
        if self.DEBUG: print ('Ready.')


    def _finish(self):
        self._epoch = time.time()
        if self.DEBUG: print('Finished.')

    
    def query_simbad_by_name(self, query: NameQuery):
        self._begin()
        if self.DEBUG: print('Querying object ', query.id)
        result = Simbad.query_object(query.id) 
        self._finish()
        return result 


    def query_simbad_by_coords(self, query: CoordsQuery):
        self._begin()
        result = Simbad.query_region(query.coords, radius=query.radius*u.arcsec)
        self._finish()
        return result 


def main():
    q = QuerySimbad(debug=True) 
    for name in TEST_NAMES:
        q.query_simbad_by_name(NameQuery(name))


if __name__ == '__main__':
    main()