import time

from time import sleep
from astropy.coordinates.sky_coordinate import SkyCoord
from astroquery.simbad import Simbad

#
# This script compares the performance of the Harvard mirror for SIMBAD compared to the 
# standard mirror, the Stasbourg mirror. The Harvard mirror is believed to improve 
# performance. 
#
# http://simbad.harvard.edu/ 
#

# Using the SIMBAD script service. 
HARVARD_MIRROR = 'http://simbad.cfa.harvard.edu/simbad/sim-script'
DEFAULT_MIRROR = 'http://simbad.u-strasbg.fr/simbad/sim-script'

# Test data.
OBJ_IDS = ['m13', 'm1', 'MAXI J1820+070']

REGION_RA = ['18 20 21.9424', '05 34 31.94', '06 45 08.91728']
REGION_DEC = ['+07 11 07.278', '+22 00 52.2', '-16 42 58.0171']
REGION_RADIUS = ['0.1', '0.3', '0.5']

def main():
    # Testing default mirror.
    print('\nTESTING: default mirror Strasbourg ->', DEFAULT_MIRROR, '\n')
    default_result_test1, default_result_test2 = run_test(DEFAULT_MIRROR)

    # Testing the Harvard mirror. 
    print('\nTESTING: Harvard mirror ->', HARVARD_MIRROR, '\n')
    harvard_result_test1, harvard_result_test2 = run_test(HARVARD_MIRROR)

    print('\nRESULTS:\n')
    print('Default mirror, test 1:', default_result_test1, 's.')
    print('Default mirror, test 2:', default_result_test2, 's.')
    print('Harvard mirror, test 1:', harvard_result_test1, 's.')
    print('Harvard mirror, test 2:', harvard_result_test2, 's.')

def run_test(mirror):
    # Set mirror URL
    Simbad.SIMBAD_URL = mirror 
    test_1_times = [] 
    test_2_times = [] 

    # Test 1: query the 3 object IDs
    for id in OBJ_IDS: 
        print(' - Running test: query object ID', id)
        prequery = time.perf_counter()
        Simbad.query_object(id) 
        result = time.perf_counter() - prequery
        test_1_times.append(result)
        print(' - Query completed in', result, 'seconds.')
        sleep(0.25) 

    # Test 2: query the 3 coordinate ranges
    for i in range(2):
        coords = SkyCoord(REGION_RA[i], REGION_DEC[i], frame='icrs', unit=('hourangle', 'deg'))
        print(' - Running test: query region', coords)
        prequery = time.perf_counter() 
        Simbad.query_region(coords, radius=REGION_RADIUS[i]+' deg')
        result = time.perf_counter() - prequery
        test_2_times.append(result)
        print(' - Query completed in', result, 'seconds.')
        sleep(0.25)

    test_1_avg = sum(test_1_times) / 3
    test_2_avg = sum(test_2_times) / 3

    return test_1_avg, test_2_avg

if __name__ == '__main__':
    main()