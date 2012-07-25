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
from sparql1_1toN3 import translate_query_to_n3
import time

import subprocess

sys.path.append("air-reasoner/")
sys.path.append("../air-policies/")
sys.path.append("../")




#SPARQL endpoint. Change address here. TODO make it melleable. 
endpoint_test_address = 'http://air.csail.mit.edu:83'

#Triple-store containing users. Also, graph where users are stored.
user_list = 'http://localhost:86'
user_graph_name_base = "<http://air.csail.mit.edu/Users/"

#endpoint min/max ranges file
default_ranges_file = "endpoint_ranges.n3"

#default location for output of query to n3 translation
default_sparql2n3_output_location = "/var/www/spim_ontologies/query_in_n3.n3"

#Location of policy_spim_run.py, which is used to run the air-reasoner on the policy. 
#CHANGE LOCATION OF FILE IF NECESSARY
policyrunnerSpim = '/home/yyyaron/spim/lib/policy_runner_spim.py'

#Information for policyrunner
logURI = "http://air.csail.mit.edu/spim_ontologies/query_in_n3.n3"
ruleURI = "http://air.csail.mit.edu/spim_ontologies/policies/internet_use_policy.n3"

class SPIM:

	#endpointAddress = address of where is being queried
	#endpointType = type of endpoint (e.g. 4store)
	#userProfileList = where the user profiles are located.

    def __init__(self, endpointAddress, endpointType, ranges_file = default_ranges_file, profileStore = user_list, profileStoreType = '4store'):
        self.endpoint = endpointFactory(endpointAddress, endpointType) #Endpoint being queried
	self.userList = endpointFactory(profileStore, profileStoreType) #Endpoint with user epsilon values
	self.endpoint_ranges = parse_ranges(ranges_file) 


    #Main method that does full query processing. Applies AIR if asked to, otherwise just differential
    #privacy.
    def acceptQuery(self, query, username, eps_cost = 1.0, base_eps = "5.0", use_air = True):

	now = time.time()
	
	#Step 1: accept user
	self.acceptUser(username, base_eps)
	
	#Step 2: Apply air if asked to. Note: AIR is run from the command line so that the reasoning
	#tree may be used by they python program.

	print "Accepting user took ", time.time() - now, "seconds"
	now = time.time()

	if use_air:
	    translate_query_to_n3(query, default_sparql2n3_output_location) #translate the query to n3
	    command = "python " + policyrunnerSpim + " '" + logURI + "' '" + ruleURI + "'"
	    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
	    output = process.communicate()[0]
	    print output
	
	    print "AIR took", time.time() - now, "time to process results"
  
	    if "air:non-compliant-with" in output:
	        toReturn = "The query is non-compliant with the data-point's air policy. See below for the reasoning tree\n"
	        toReturn += output
	        return toReturn



	#Step 3: Apply differential privacy
	return self.applyDifferentialPrivacy(query, username, eps_cost)


    #Function that accepts a username and some base epsilon budget and allocates a username for it if it does
    #not exist.
    def acceptUser(self, username, base_eps = 5.0):
	
	#Part 1: Create user profile if it doesn't exist in triplesotre	
	userURI = user_graph_name_base + username + '/' + username + '>'
	
	#Make user graph name
	user_graph_name = user_graph_name_base + username + ">"

	#Check if user profile exists

	query_for_profile = 'SELECT * WHERE {' + userURI + ' ?p ?o}' 
	user_profile_result = self.userList.sendQuery(query_for_profile)

	if user_profile_result == None or len(user_profile_result) == 0:
		self.addUser(username, base_eps)

    def applyDifferentialPrivacy(self, query, username, eps_cost = 1.0):

	now = time.time()

  	userURI = user_graph_name_base + username + '/' + username + '>'
	eps = eps_cost #artifact, was using eps as variable name everywhere. Fix

	#Minimum eps value is the most recent one, so get it. A more elegant solution is to delete old eps values, though i ran into some problems with that. For a future implementation.

	query_for_epsValue = "SELECT (MIN(?o) as ?minimum) WHERE {" + userURI + " <http://air.csail.mit.edu/SPIM/epsValue> ?o}"

	user_result = self.userList.sendQuery(query_for_epsValue)
	
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
#	    print "EPSILON EXCEEDED"

	#Part 4: Calc query sensitivity
	

        allVariables = sparqlParser.extractAllVars(query)
	whereClause = sparqlParser.extractWhere(query)
	query_sensitivity_all = self.calc_func_sensitivity(whereClause, allVariables, query)
	query_sensitivity = query_sensitivity_all
#	print query_sensitivity_all

	#Send query 

	result = self.endpoint.sendQuery(query)

	query_time = time.time() - now

	print "Time for query was", query_time

	print result
	for t in result: #Iterate over terms from query
	    for tag in allVariables:
		tagVars = allVariables[tag]
            	for c in tagVars: #Check over variables found
                    if c in t:
                    	counted = float(t[c])
                    	t[c] = user.addNoise(counted, eps, query_sensitivity)
	#Update eps value in triple store
	newEps = currEps - eps
	print "New eps: ", newEps

	print "Time to do differential privacy was", time.time() - query_time - now, "seconds"

	#In a future implementation, this deletion should be made correct and addee back in.
#	triple_to_remove = userURI + ' <http://air.csail.mit.edu/SPIM/epsValue> "' + str(currEps) + '"'
#	self.userList.delete_from_graph(user_graph_name, triple_to_remove)

	#Add new eps value
	self.addUser(username, newEps)
	print "Finished<br>"
        return result

    def addUser(self, username, maxEps):
	user_graph_name = user_graph_name_base + username + "/" + username + ">"
	triple_to_add = user_graph_name + ' <http://air.csail.mit.edu/SPIM/epsValue> "' + str(maxEps) + '".' 
        self.userList.append_graph(user_graph_name, triple_to_add)
	print triple_to_add

	#Calculates the function's sensitivity. 
    def calc_func_sensitivity(self, whereClause, allVars, query):
	sens = 1.0
	testR =  self.endpoint.sendQuery(query)
	for v in allVars:
	    if len(allVars[v]) > 0:	#We need to calculate this
		if v == "COUNT":
		    continue
		elif v == "SUM":		#Calculate SUM clause
		    sums = sparqlParser.extract_all_sum(query)		 		
		    for s in sums: #Calc sum by finding the max of the variable
			#Rewrite query to be able to find suitable sensitivity for given variable.
			newS = "(MAX" + s[4:] 
			newQuery = "SELECT " + newS + " " + whereClause

			#Calculate sensitivity
			newSens = 1.0
			#print newQuery
			result = self.endpoint.sendQuery(newQuery)
			if result == None or len(result) == 0:
			    print "No sensitivity returned"
			else:
			    result = result[0]
			    for r in result:
				try:
				    newSens = float(result[r])
				except:
				    print "Error: Sensitivity from SUM is not numeric"

			if newSens > sens:
			    sens = newSens
			 #   print "New sens is", newSens

		elif v == "AVG": #Calculate AVG sensitivity
		    newSens = 1.0
		    avgs = sparqlParser.extract_all_avg(query)
		    for a in avgs:
			newS = "(COUNT" + a[4:8] + " as ?one) (MIN" + a[4:8] + " as ?minimum)"
			newQuery = "SELECT " + newS + " " + whereClause

			#Calculate new sensitivity
			newSens = 1.0
			#print newQuery
			result = self.endpoint.sendQuery(newQuery)
			if result == None or len(result) == 0:
			    print "No sensitivity returned"
			else:
			    result = result[0]
			    #try:
		     	    print result
			    totalSize = result['one']
			    try:
				totalSize = float(result['one'])
				minValue = float(result['minimum'])
				newSens = totalSize / minValue
				print "Sens from AVG is", newSens
			    except:
				print "Error: Sensitivity from AVG is not numeric"
			
			if newSens > sens:
			    sens = newSens
			  #  print "New sens is", newSens
		#Calculate sensitivity on MAX or MIN
		elif v == "MAX" or v == MIN:
		    newSens = 1.0
		    maxes = sparqlParser.extract_all_max(query)
		    for m in maxes:
			result = self.endpoint.sendQuery(query)
			if result == None or len(result) == 0:
			    print "No Sensitivity Returned on MIN"
			else:
			    result = result[0]
			    for r in result:
				try:
				    newSens = float(result[r])
				except:
				    print "Error: Sensitivity from MAX is not numeric"
			if newSens > sens:
			    sens = newSens
		    
	return sens
     
#Adds key to dictionary if not there, or increments count of key by one
def incrementKey(dic, key):
    if key in dic:
        dic[key]+= 1
    else:
        dic[key] = 1

#Parses the file of endpoint ranges and returns min/max dictionaries with predicate names as keys
def parse_ranges(endpoint_ranges_file = default_ranges_file):
	toReturn = {}
	f = open(endpoint_ranges_file, 'r')	
	for line in f:
	    words = line.split()
	    if len(words) == 0:
		continue
	    toReturn[words[0]] = {}
	    for i in range(len(words)):
		word = words[i]
		if word == "pred:max":
	            toReturn[words[0]][word] = words[i+1]
		if word == "pred:min":
		    toReturn[words[0]][word] = words[i+1]
	return toReturn
	


def main(args = 'user0'):


    endpoint_test_address = 'http://air.csail.mit.edu:81'
    query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT (MAX(?o) as ?size) (AVG(?o) as ?b) WHERE {
 ?s <http://data-gov.tw.rpi.edu/vocab/p/10040/principal_city_internet_use_anywhere> ?o 
	FILTER(isNumeric(?o))
}"""
    print query
    spim = SPIM(endpoint_test_address, '4store')
    pprint(spim.acceptQuery(query, args))

if __name__ == '__main__':
    if(len(sys.argv) > 1):
	main(sys.argv[1])
    else:
	main()




