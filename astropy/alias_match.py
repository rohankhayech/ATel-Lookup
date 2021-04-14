from astroquery.simbad import Simbad

'''
''  This method returns a Python list of object aliases
''  if the object is in the SIMBAD database, or 
''  None if the object D.N.E.
'''
def get_aliases(id):
    # Query SIMBAD
    result = Simbad.query_objectids(id) 
    if (result == None):
        # Object not found.
        return None 
    else:
        lst = []
        for line in str(result).splitlines(): 
            value = line.strip() 
            # Ignore table heading.
            if value != 'ID' and not value.startswith('--'):
                lst.append(value)
        return lst 

print (get_aliases('m13'))