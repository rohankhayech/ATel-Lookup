import re

'''
    Loads body text from file.

    :param: Filename

    :return: Body text from file
    :rtype: String
'''
def loadBodyText(filename):
    with open(filename) as file:
        body = file.read()
    return body


'''
    Finds all date strings with the format '2021-02-02 04:59' in the body text.

    :param body: Body text to search.
    :type: string

    :return: List of date strings found.
'''
def findDates(body):
    dateRegex = re.compile('[1-2]\d\d\d-[0-1]\d-[0-3][0-9]\s[0-2]\d:[0-5]\d')

    datesFound = dateRegex.findall(body)

    return datesFound

'''
    Finds all coordinates in sexagesimal RA DEC formats.

    :param body: Body text to search.
    :type: string

    :return: List of coordinate strings found.
'''
def findCoords(body):
    coordRegex = re.compile('RA:?\s*\d\d[:h\s]\d\d[:m\s]\d\d(?:.\d*s?)?,?\s*Dec:?\s*[\+-]?\d\d[:h\s]\d\d[:m\s]\d\d(?:.\d*s?)?')
    
    # standard regex as works in regexr, however groups eg. (group) have to be 'non-capturing' groups eg. (?:group)
    # so that findall will return the whole matching string

    coordsFound = coordRegex.findall(body)

    return coordsFound

# Main 
body = loadBodyText('atel14573.txt')
body2 = loadBodyText('example-coords.txt')

print('\n')
print("Dates found: "+str(findDates(body)))
print('\n')
print("Coords found: "+str(findCoords(body2)))
print('\n')