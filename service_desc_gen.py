#Create a service description file for a SPARQL 4store endpoint. Code makes
#use of Endpoint module, and so may be suitable for other types of endpoints.
#However, these must be compatible with RDFLib.

from endpoint import Endpoint4Store
import rdflib

def create_service_description(endpointAddress, file_name = "service_description.n3"):
    endpoint = Endpoint4Store(endpointAddress)

    #Step 1: Get all the predicates
    #SECURITY HAZARD: Might not get all predicates, in which cast this will be
    #exploitable. TODO fix it
    predicate_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2001/rdf-schema#>

SELECT DISTINCT ?p WHERE {
 ?s ?p ?o.
 FILTER(isNumeric(?o))
}
"""
    predicates = endpoint.sendQuery(predicate_query)
    #print predicates
    allPredicates = {}

    #Iterate through the predicates to calculate the function sensitivities
    for p in predicates:
        predicate = p['p']
	print predicate
        query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2001/rdf-schema#>

SELECT (MAX(ABS(?o)) as ?max) (MIN(ABS(?o)) as ?min) WHERE {
 ?s <""" + p['p'] + """> ?o
}
"""
        
        #allPredicates[p['p']] = p['p']
        allPredicates[predicate] = {}
        result = endpoint.sendQuery(query)
        
        term = result[0]
        allPredicates[predicate]['max'] = term['max']
        allPredicates[predicate]['min'] = term['min']
        
##        i = 0
##        try:
##            i = int(term['max'])
##        except ValueError:
##            try:
##                i = float(term['max'])
##            except:
##                i = None

    print allPredicates
    
    file_header = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix pred: <http://air.csail.mit.edu/spim/predicate_desc.n3#>.


"""
    f = open(file_name, 'w')
    f.write(file_header)
    for p in allPredicates:
        f.write(str(p) + " pred:max " + str(allPredicates[p]['max']) + ';\n')
        f.write("\t pred:min " + str(allPredicates[p]['min']) + '.\n')



def main():
    print "STARTING GENERATION"
    test_address = "http://air.csail.mit.edu:81"
    create_service_description(test_address)



if __name__ == "__main__":
    main()
