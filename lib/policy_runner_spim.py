import sys


sys.path.append("air-reasoner")

import policyrunner

defaultLogURI = ["http://air.csail.mit.edu/spim_ontologies/query_in_n3.n3"]
#ruleURI = ["http://air.csail.mit.edu/spim_ontologies/policies/check_if_query_policy.n3"]
defaultRuleURI = ["http://air.csail.mit.edu/spim_ontologies/policies/internet_use_policy.n3"]

#logURI = ['http://air.csail.mit.edu/spim_ontologies/examples/basic_log.n3']
#ruleURI = ['http://air.csail.mit.edu/spim_ontologies/examples/basic_rule.n3']

#For command line arguments, first argument should be the log uri, second should be the rule uri. Did not
#handle any extra inputs, but should not be hard to extend this script.

def run_spim_policy():

    print sys.argv
    if len(sys.argv) == 1:
	return policyrunner.runPolicy(defaultLogURI, defaultRuleURI, verbose=True)
    
    if len(sys.argv) == 2:
	raise Exception("Error: Requires two filenames, one logURI and one ruleURI")

    else:
	logURI = [sys.argv[1]]
	ruleURI = [sys.argv[2]]
	return policyrunner.runPolicy(logURI, ruleURI, verbose=True)

def main():
    return run_spim_policy()

if __name__ == "__main__":
    main()


