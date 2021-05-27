import sys 
import time
import warnings
import astropy.units as u
from astropy import units 
from progress.bar import ChargingBar
from astroquery.simbad import Simbad 
from astropy.coordinates import SkyCoord 


DELAY_INTERVAL = 0.25 # Equivalent to 4 queries per second. 


DATA_SET = [ # Fixed data set -- See report document associated w/ this. 
    SkyCoord('17 08 57', '-32 29 41', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('270.80', '29.80', frame='icrs', unit=('deg', 'deg')),
    SkyCoord('18 10 44.47', '-26 09 01.2', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('17 45 40.1640', '-29 00 29.818', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('09 55 33.17306143', '+69 03 55.0609270', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('16.30', '+34.23', frame='icrs', unit=('deg', 'deg')),
    SkyCoord('05 10 44.200', '-31 35 37.61', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('17 13 49.53053', '+07 47 37.5264', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('11 39 50.482', '-07 36 26.76', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('00 30 17.4924122720', '-42 24 46.484822351', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('19 07 58.625', '+08 43 45.14', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('04 05 15.30', '-74 51 58.1', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('78.938767', '-45.945369', frame='icrs', unit=('deg', 'deg')),
    SkyCoord('255.0387208', '68.5019331', frame='icrs', unit=('deg', 'deg')),
    SkyCoord('13 48 56.75', '+26 39 46.8', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('91.76', '9.52', frame='icrs', unit=('deg', 'deg')),
    SkyCoord('12 35 52.300', '+27 55 55.50', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('05 15 45.2500502966', '-45 56 43.201382295', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('17 00 09.2929719245', '+68 30 06.958673355', frame='icrs', unit=('hourangle', 'deg')),
    SkyCoord('09 48 38.860', '+33 25 03.18', frame='icrs', unit=('hourangle', 'deg'))
]


def main():
    # Ignore regions that have no objects found.
    # In the real product, we would handle this instead. 
    # A UserWarning is raised by astroquery if it an object isn't found. 
    warnings.filterwarnings('ignore')

    if len(sys.argv) != 2:
        print ('Usage: python3 mass-search.py [NUM-QUERIES]')
    elif len(sys.argv) == 2: 
            proceed = input ('WARNING: This script may result in a temporary IP blacklist\n' +
                'from the SIMBAD server for approximately 1 hour. Use at your own risk.\n' +
                'This script is designed for testing purposes only. Continue? [Y/N]: '
            )

            if proceed == 'Y':
                run_test(int(sys.argv[1]))


def run_test(num_queries: int): 
    if not num_queries in range(1, 10000):
        raise RuntimeError('NUM-QUERIES not in range 1 -> 10,000')
    prev_time = time.time()
    with ChargingBar('Executing queries', max=num_queries) as bar:
        for i in range(num_queries):
            try:
                do_query(DATA_SET[i % len(DATA_SET)]) 
                time.sleep(DELAY_INTERVAL) # NOT thread safe, do NOT use in the product!!
                bar.next()
            except ConnectionError as e:
                print ('TEST FAILED You may have been blacklisted!:', e.strerror)
                raise e
    time_taken = time.time() - prev_time
    print ('TEST SUCCESSFUL: executed', num_queries, 'queries in', time_taken, 'seconds.')

def do_query(q: SkyCoord):
    Simbad.query_region(q, radius=0.00277778*u.deg) # == 10 arcseconds

if __name__ == '__main__':
    main()