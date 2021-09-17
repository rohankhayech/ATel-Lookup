from astroquery.simbad import Simbad as simbad
import random
import string
import warnings
from progress.bar import ChargingBar


#
# SIMBAD Stress Test 
#


def gen_random_name():
    return ''.join(random.choices(string.ascii_uppercase, k=10))


def main():
    warnings.filterwarnings('ignore')

    proceed = input("""WARNING: This script is experimental, and may result in an 
        IP ban from the SIMBAD astronomical database. This ban is temporary, 
        however there may be undocumented implications. Continue at your
        risk. Continue? [y/n]: 
        """)
    proceed = proceed == 'Y' or proceed == 'y'

    if not proceed:
        return 

    num_queries = int(input("How many queries to execute?: "))

    if not num_queries > 0:
        raise ValueError("Number of queries must be > 0")

    with ChargingBar('Executing queries...', max=num_queries) as bar:
        for _ in range(num_queries):
            try:
                simbad.query_object(gen_random_name())
                bar.next()
            except ConnectionError as e:
                print("TEST FAILED: you may have been blacklisted.")
                raise e


if __name__ == '__main__':
    main()