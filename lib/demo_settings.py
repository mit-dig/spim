from endpoint import endpointFactory

##These next few are configurations

UNIQUE_PERSON_IDENTIFIER = "foaf:name"

#SPARQL endpoint. Change address here. TODO make it melleable. 
endpoint_test_address = 'http://air.csail.mit.edu:81'

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

#Default Information for policyrunner
logURI = "http://air.csail.mit.edu/spim_ontologies/query_in_n3.n3"
ruleURI = "http://air.csail.mit.edu/spim_ontologies/policies/internet_use_policy.n3"

users_demo = ["Alice", "Bob", "Charlie"]

policy_for_user = {"Alice": "",
                   "Bob": "http://air.csail.mit.edu/spim_ontologies/policies/bob_policy.n3",
                   "Charlie": "http://air.csail.mit.edu/spim_ontologies/policies/hipaa_policy.n3"
                   
                   }

eps_for_user = {"Alice": -1.0,
                    "Bob": 0.5,
                    "Charlie": 0.5
                    }
                    
def add_demo_users(userList):
    endpoint = endpointFactor(endpoint_test_address, '4store')
    userList = endpointFactory(user_list, '4store')
    for username in users_demo:
	user_graph_name = user_graph_name_base + username + "/" + username + ">"
	maxEps = eps_for_user[username]
	triple_to_add = user_graph_name + ' <http://air.csail.mit.edu/SPIM/epsValue> "' + str(maxEps) + '".' 
        self.userList.append_graph(user_graph_name, triple_to_add)
	print triple_to_add        


def set_up_for_demo():
    add_demo_users()


if __name__ == "__main__":
    set_up_for_demo()
