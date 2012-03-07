##The central module of the SPARQL endpoint privacy assurance module. This
##module will mediate betweent the different python modules, assuring that both
##compliance in AIR is achieved and that differential privacy is assured.

##Is of a server form. It will listen 

from endpoint import endpointFactory
from pprint import pprint
from userManager import UserManager, UserProfile
import re
import sparqlParser

#SPARQL endpoint. Change address here. TODO make it melleable. 
endpoint_test_address = 'http://air.csail.mit.edu:83'

#Triple-store containing users. Also, graph where users are stored.
user_list = 'http://localhost:86/"
user_graph_name = "http://air.csail.mit.edu/Users"

class SPIM:
	#endpointAddress = address of where is being queried
	#endpointType = type of endpoint (e.g. 4store)
	#userProfileList = where the user profiles are located.
    def __init__(self, endpointAddress, endpointType, profileStore = user_list, profileStoreType = '4store',
					userGraphName = user_graph_name):
        self.endpoint = endpointFactory(endpointAddress, endpointType) #Endpoint being queried
	self.userList = endpointFactory(profileStore, profileStoreType) #Endpoint with user epsilon values
	self.userGraphName = userGraphName #Graph name with user info

    def acceptQuery(self, query, username, eps = 1.0):
	
	#Check if user profile exists
	query_for_profile = 'SELECT * WHERE {<http://air.csail.mit.edu/Users/' + username + ' ?p ?o}' 

	user = self.userList.getUser(username)
        if user.epsExceeded(eps):
            print "EPSILON EXCEEDED"
            return
        countVariables = sparqlParser.extractAllVars(query) #Extract which variables are count
        result = self.endpoint.sendQuery(query)
	for t in result: #Iterate over terms from query
	    for tag in countVariables:
		tagVars = countVariables[tag]
            	for c in tagVars: #Check over variables found
                    if c in t:
                    	counted = int(t[c])
                    	t[c] = user.addNoise(counted, eps)
        return result

    def addUser(self, username, maxEps):
	triple_to_add = '<http://air.csail.mit.edu/Users/' + username + ' <http://air.csail.mit.edu/SPIM/epsValue> "' + maxEps + '".' 
        self.userList.append_graph(self.userGraphName, triple_to_add)
     
#Adds key to dictionary if not there, or increments count of key by one
def incrementKey(dic, key):
    if key in dic:
        dic[key]+= 1
    else:
        dic[key] = 1

def main():
    endpoint_test_address = 'http://air.csail.mit.edu:83'
    query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT (COUNT(?p) as ?size) WHERE {
 ?s ?p ?o
} LIMIT 1000
"""
    spim = SPIM(endpoint_test_address, '4store')
    spim.addUser('user0', 5.0)
    pprint(spim.acceptQuery(query, 'user0'))

if __name__ == '__main__':
    main()
