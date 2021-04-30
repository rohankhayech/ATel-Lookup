import re 

from astropy import units as u 

# Validates RA/DEC/Radius in sexagesimal or floating point value. 
# Demonstrates regex patterns, radius must be 
#
# Author:       Ryan Martin
# Date created: 30/04/2021

# [float]h[float]m[float]s
RA_REGEX = re.compile('[0-9]+(\.[0-9]+)?h[0-9]+(\.[0-9]+)?m[0-9]+(\.[0-9]+)?s')
# [float]d[float]m[float]s
DEC_REGEX = re.compile('[0-9]+(\.[0-9]+)?d[0-9]+(\.[0-9]+)?m[0-9]+(\.[0-9]+)?s')
#
# For all of these validation functions, they will return u.deg (decimal degrees)
# defined in the astroquery.units module (you may see a Module has no member error in 
# your IDE, however it seems to be a bug). If not float, return None for 
# sexagesimal notation. 
#
# The reason we need to return the units in these methods is because the units
# must be defined in a vector for the Simbad query methods that correlates to 
# each value. 
#
# The units are invalid if the function returns False. 
#
def validRA(ra_value):
    if (isFloat(ra_value)):
        return u.deg
    else:
        if re.match(RA_REGEX, ra_value):
            return None
    return False 

def validDEC(dec_value):
    if (isFloat(dec_value)):
        return u.deg
    else:
        if re.match(DEC_REGEX, dec_value):
            return None
    return False 

def validRadius(rad_value):
    if isFloat(rad_value):
        if float(rad_value) <= 0.5 and float(rad_value) >= 0.0:
            return u.deg
    return False

def isFloat(value):
    try:
        float(value) 
        return True 
    except ValueError:
        return False 

def main():
    ra = input('RA: ')
    dec = input('DEC: ')
    rad = input('Radius: ')

    print('RA:', validRA(ra))
    print('DEC:', validDEC(dec))
    print('Radius:', validRadius(rad))

if __name__ == '__main__':
    main()