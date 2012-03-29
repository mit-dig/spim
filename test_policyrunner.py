import sys
sys.path.append("lib/air-reasoner/")
from policyrunner import testpolicy
sys.path.append("air-policies/")

policy = "census_policy1.n3"

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX census: <tag:govshare.info,2005:rdf/census/>

SELECT * WHERE {
 ?s census:population ?o
}"""

testpolicy(query, 

