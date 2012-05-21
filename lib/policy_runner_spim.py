import sys

sys.path.append("air-reasoner")

import policyrunner

logURI = ["http://air.csail.mit.edu/spim/lib/query_translation.n3"]
ruleURI = ["http://air.csail.mit.edu/spim/policies/internet_use_policy.n3"]

def main():
#    policyrunner.OFFLINE[0] = True
    policyrunner.runPolicy(logURI, ruleURI, verbose=True)


if __name__ == "__main__":
    main()


