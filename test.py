import cowardin_to_osm

decoder = cowardin_to_osm.cowardin_decoder()

code = input('Enter a Cowardin wetland code:')
tags = decoder.code_to_tags(code)
print(tags)