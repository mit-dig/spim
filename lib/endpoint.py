from pprint import pprint
from HTTP4Store import HTTP4Store
import os

#Interface for a query endpoint. Needs to accept an endpoint location on
#construction, and get a query result.
class Endpoint:
    def __init__(self, endpointAddress):
        self.address = endpointAddress
	self.type = "None"
    def sendQuery(self, query):
        return None
    def getStatus(self):
        return None
    def getAddress(self):
        return self.address
    #Append ONE triple to a graph
    def append_graph(self, graph_name, triples):
	return
    def delete_graph(self, graph_name, tripes):
	return


#Creates an object with a connection to a 4store interface
class Endpoint4Store(Endpoint):
    def __init__(self, endpointAddress):
        self.address = endpointAddress
        self.endpoint = HTTP4Store(endpointAddress)
	self.type = '4store'

    def sendQuery(self, query): #Query the
        return self.endpoint.sparql(query)
    def getStatus(self):
	return self.endpoint.status()
    def getAddress(self):
	return self.address
    def append_graph(self, graph_name, triples):
	#First, replace spaces with '+' to comply with syntax
	tripes = triples.replace(' ', '+')
	command = "update=INSERT+DATA+{+GRAPH+" + graph_name + "+{+" + triples + "+}+}"
	os.system("curl -i -d '" + command + "' http://localhost:86/update/")			
    def delete_from_graph(self, graph_name, triples):
	#Replace spaces in triple
	triples = triples.replace(' ', '+')
	command = "update=DELETE+DATA+{GRAPH+" + graph_name +  "+{+" + triples + "+}+}"
	os.system("curl -i -d '" + command + "' httpd://localhost:86/update/")




#General method to make an endpoint interface. By default, and object of
#the superclass is made. 
def endpointFactory(endpointAddress, sparql_type):
    if sparql_type == '4store':
        return Endpoint4Store(endpointAddress)
    else:
        return Endpoint(endpointAddress)


def main():
    query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT (COUNT(?s) as ?size) WHERE {
 ?s ?p ?o
} LIMIT 10
"""
    e = Endpoint4Store('http://air.csail.mit.edu:82')
    pprint(e.sendQuery(query))
    
if __name__ == '__main__':
    main()
