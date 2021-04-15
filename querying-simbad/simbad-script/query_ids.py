import requests 

'''
    A Python script that demonstrates a script request to SIMBAD that gets the
    aliases for an object. 

    author: Ryan Martin 
'''

# The URL script. Requires the object ID to be appended to the end to work. 
_URL = "http://simbad.u-strasbg.fr/simbad/sim-script?script=format%20object%20%22%25IDLIST%22%0a"

def get_aliases_list(id):
    # Append id to URL
    url = _URL + id 
    list = [] 
    # HTML POST request 
    data = requests.request('POST', url)

    if (data.content != None):
        # Convert bytes to string 
        content = data.content.decode('utf-8')
        # Convert string to list
        content_split = content.splitlines() 
        i = 0

        # Ignore everything up to the data section. 
        while (content_split[i].startswith("::data") == False):
            i = i + 1
        i = i + 2

        # Construct a list of the aliases.
        while (i < content_split.__len__()):
            list.append(content_split[i])
            i = i + 1

    return list 

result = get_aliases_list("m13")
print(result)