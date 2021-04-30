import re 

# Validates RA/DEC/Radius in sexagesimal or floating point value. 
# Demonstrates regex patterns, radius must be 
#
# Author:       Ryan Martin
# Date created: 30/04/2021

# [float]h[float]m[float]s
RA_REGEX = re.compile('[0-9]+(\.[0-9]+)?h[0-9]+(\.[0-9]+)?m[0-9]+(\.[0-9]+)?s')
# [float]d[float]m[float]s
DEC_REGEX = re.compile('[0-9]+(\.[0-9]+)?d[0-9]+(\.[0-9]+)?m[0-9]+(\.[0-9]+)?s')

def validRA(ra_value):
    if (isFloat(ra_value)):
        return True 
    else:
        if re.match(RA_REGEX, ra_value):
            return True
    return False 

def validDEC(dec_value):
    if (isFloat(dec_value)):
        return True 
    else:
        if re.match(DEC_REGEX, dec_value):
            return True
    return False 

def validRadius(rad_value):
    if isFloat(rad_value):
        if float(rad_value) <= 0.5 and float(rad_value) >= 0.0:
            return True 
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

    if not validRA(ra): 
        print('Invalid RA value!')
    else:
        print('RA = valid')
    if not validDEC(dec):
        print('Invalid DEC value!')
    else:
        print('DEC = valid')
    if not validRadius(rad):
        print('Invalid radius value!')
    else:
        print('Radius = valid')

if __name__ == '__main__':
    main()