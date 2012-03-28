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
#Note: Triples must only use whitespaces, and must be written on ONE LINE. 
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

	##HUGE SECURITY RISK!! Sudo + user-inputted username. Might be very bad

    def append_graph(self, graph_name, triples):
	print graph_name
	self.endpoint.append_graph(graph_name, triples)

    def delete_from_graph(self, graph_name, triples):
	#query = "DELETE { GRAPH " + graph_name + " { " + triples + " } }"
	print graph_name
	self.endpoint.del_graph(graph_name)
	#print query

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
    e = Endpoint4Store('http://air.csail.mit.edu:86')
    pprint(e.sendQuery(query))
    print "Update test" 
    print e.endpoint.status()
    f = Endpoint4Store('http://localhost:86')
    triple = '<http://example.com/Yotam> <http://example.com/epsValue> "1.0"'
#    triple = '<httpd://example.com/s>+<http://example.com/p>+"o"'
    f.append_graph("http://default.org", triple)
    query2 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT * WHERE {
 ?s ?p ?o
} LIMIT 10
"""
    pprint(f.sendQuery(query2))
    f.delete_from_graph("http://default.org", triple)
    pprint(f.sendQuery(query2))
    
if __name__ == '__main__':
    main()
