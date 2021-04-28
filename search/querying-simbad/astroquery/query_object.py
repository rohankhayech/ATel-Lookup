from astroquery.simbad import Simbad 

# Query object 'm13' and put the result into a Table object:
table = Simbad.query_objectids("m13")

# Print the string representation of the table:
# print(table)

# Query the field "DEC":

print(table)