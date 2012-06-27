import sys

sys.path.append("air-reasoner")

import policyrunner

#logURI = ["http://air.csail.mit.edu/spim_ontologies/query_in_n3.n3"]
ruleURI = ["http://air.csail.mit.edu/spim_ontologies/policies/internet_use_policy.n3"]

logURI = ['http://air.csail.mit.edu/spim_ontologies/examples/basic_log.n3']
#ruleURI = ['http://air.csail.mit.edu/spim_ontologies/examples/basic_rule.n3']

def main():
    policyrunner.runPolicy(logURI, ruleURI, verbose=True)


if __name__ == "__main__":
    main()


