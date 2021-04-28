import requests

'''
''  Querying TAP example. 
''  Example: find the alises of 'm13', download as a CSV file. 
''  author: Ryan Martin. 
'''

# URL for SIMBAD TAP query:
_QUERY_URL = "http://simbad.u-strasbg.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=csv&query="
# Query for related aliases:
_QUERY_IDS = "SELECT%20id2.id%20FROM%20ident%20AS%20id1%20JOIN%20ident%20AS%20id2%20USING(oidref)%20WHERE%20id1.id%20=%20%27"

def query_objectids(id):
    lst = []

    # url + query + id + terminator
    url = _QUERY_URL + _QUERY_IDS + id + "%27;"
    data = requests.request('POST', url) 
    result = data.content.decode('utf-8') 

    if (result != None):
        for line in result.splitlines():
            if (line != 'id'):
                lst.append(line) 

    return lst 

result = query_objectids('m13') 
print(result) 