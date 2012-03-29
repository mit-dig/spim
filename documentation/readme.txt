



KNOWN BUG FIXES:

1- HTTP4Store del_graph bug:
Old versions of HTTP4Store will have a bug where deleting from a graph causes an error. To fix it, 
find where HTTP4Store is installed on you machine. In HTTP4Store.py, under the function "del_graph", 
change "self.sparql_endpoint" to "self.data_endpoint." 
