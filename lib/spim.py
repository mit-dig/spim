#The central module of the SPARQL endpoint privacy assurance module. This
##module will mediate betweent the different python modules, assuring that both
##compliance in AIR is achieved and that differential privacy is assured.

##Is of a server form. It will listen 

from endpoint import endpointFactory
from pprint import pprint
from userManager import UserManager, UserProfile
import re
import sparqlParser
import sys

sys.path.append("air-reasoner/")
sys.path.append("../air-policies/")
sys.path.append("../")


#SPARQL endpoint. Change address here. TODO make it melleable. 
endpoint_test_address = 'http://air.csail.mit.edu:83'

#Triple-store containing users. Also, graph where users are stored.
user_list = 'http://localhost:86'
user_graph_name_base = "<http://air.csail.mit.edu/Users/"

policy_file = "census_policy1.n3"


class SPIM:
	#endpointAddress = address of where is being queried
	#endpointType = type of endpoint (e.g. 4store)
	#userProfileList = where the user profiles are located.
    def __init__(self, endpointAddress, endpointType, profileStore = user_list, profileStoreType = '4store'):
        self.endpoint = endpointFactory(endpointAddress, endpointType) #Endpoint being queried
	self.userList = endpointFactory(profileStore, profileStoreType) #Endpoint with user epsilon values

    def acceptQuery(self, query, username, eps = 1.0):

	#Part 1: Create user profile if it doesn't exist in triplesotre	
	userURI = user_graph_name_base + username + '/' + username + '>'
	
	#Make user graph name
	user_graph_name = user_graph_name_base + username + ">"

	#Check if user profile exists

	query_for_profile = 'SELECT * WHERE {' + userURI + ' ?p ?o}' 
	user_profile_result = self.userList.sendQuery(query_for_profile)

	if user_profile_result == None or len(user_profile_result) == 0:
#		print "Adding user"
		self.addUser(username, 5.0)

	#Minimum eps value is the most recent one, so get it. A more elegant solution is to delete old eps values, though i ran into some problems with that. For a future implementation.

	query_for_epsValue = "SELECT (MIN(?o) as ?minimum) WHERE {" + userURI + " <http://air.csail.mit.edu/SPIM/epsValue> ?o}"

	user_result = self.userList.sendQuery(query_for_epsValue)
	
	#Part 2: 
	#Part 3: Create object to manage differential privacy

	#TODO Cache users

	#Create user profile
	currEps = user_result[0]['minimum']
	currEps = str(currEps)[1:len(currEps)-1]
	currEps = float(str(currEps))

	#Check if epsilon has been exceeded
	user = UserProfile(username, currEps)		
        if user.epsExceeded(eps):
            return "EPSILON EXCEEDED"

        countVariables = sparqlParser.extractAllVars(query) #Extract which variables are count
        result = self.endpoint.sendQuery(query)
	for t in result: #Iterate over terms from query
	    for tag in countVariables:
		tagVars = countVariables[tag]
            	for c in tagVars: #Check over variables found
                    if c in t:
                    	counted = int(t[c])
                    	t[c] = user.addNoise(counted, eps)
	#Update eps value in triple store
	newEps = currEps - eps
#	print "New eps: ", newEps

	#In a future implementation, this deletion should be made correct and addee back in.
#	triple_to_remove = userURI + ' <http://air.csail.mit.edu/SPIM/epsValue> "' + str(currEps) + '"'
#	self.userList.delete_from_graph(user_graph_name, triple_to_remove)

	#Add new eps value
	self.addUser(username, newEps)
#	print "finished"
        return result

    def addUser(self, username, maxEps):
	user_graph_name = user_graph_name_base + username + "/" + username + ">"
	triple_to_add = user_graph_name + ' <http://air.csail.mit.edu/SPIM/epsValue> "' + str(maxEps) + '".' 
        self.userList.append_graph(user_graph_name, triple_to_add)
	print triple_to_add
     
#Adds key to dictionary if not there, or increments count of key by one
def incrementKey(dic, key):
    if key in dic:
        dic[key]+= 1
    else:
        dic[key] = 1

def main(args = 'user0'):



    endpoint_test_address = 'http://air.csail.mit.edu:83'
    query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT (COUNT(?p) as ?size) WHERE {
 ?s ?p ?o
} LIMIT 1000
"""
    spim = SPIM(endpoint_test_address, '4store')
    pprint(spim.acceptQuery(query, args))

if __name__ == '__main__':
    if(len(sys.argv) > 1):
	main(sys.argv[1])
    else:
	main()




