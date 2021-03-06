###############################################################
## This file contains the test queries for testing spim. The
## Q1 - Q_n series are for sensitivity testing. The P_i
## series are for testing correctness. 
###############################################################



Q1 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?e) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
        }
"""
QU1 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?e) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            MINUS {?s foaf:name "%s"}
        }
"""

########################################

Q2 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 "Insulin".
            ?e mimic:v1 ?o.
            FILTER(isNumeric(?o))
        }

"""

QU2 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 "Insulin".
            ?e mimic:v1 ?o.
            FILTER(isNumeric(?o))
            MINUS {?s foaf:name "%s"}
        }
"""

######################################

Q3 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 "Insulin".
            ?e mimic:v1 ?o.
            ?s mimic:zip "02139".
            FILTER(isNumeric(?o))
        }
"""

QU3 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 "Insulin".
            ?e mimic:v1 ?o.
            ?s mimic:zip "02139".
            FILTER(isNumeric(?o))
            MINUS {?s foaf:name "%s"}
        }

"""

########################################

Q4 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 "Insulin".
            ?e mimic:v1 ?o.
            FILTER(isNumeric(?o)).
            FILTER(?o > 1)
        }
"""

QU4 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 "Insulin".
            ?e mimic:v1 ?o.
            FILTER(isNumeric(?o)).
            FILTER(?o > 1)
            MINUS {?s foaf:name "%s"}
        }
"""

########################################

Q5 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 ?m. 
            ?e mimic:v1 ?o.
            ?e mimic:m2 ?m2.
            ?e mimic:v2 ?o2.
            FILTER(isNumeric(?o)).
            FILTER(?o > 1)
        }
"""

QU5 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 ?m. 
            ?e mimic:v1 ?o.
            ?e mimic:m2 ?m2.
            ?e mimic:v2 ?o2.
            FILTER(isNumeric(?o)).
            FILTER(?o > 1)
            MINUS {?s foaf:name "%s"}
        }
"""

#########################################

Q6 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:time ?t.
            ?e mimic:u1 ?u1.
            ?e mimic:u2 ?u2.
            ?e mimic:rt ?rt.
            ?e mimic:m1 ?m. 
            ?e mimic:v1 ?o.
            ?e mimic:m2 ?m2.
            ?e mimic:v2 ?o2.
            FILTER(isNumeric(?o2) && isNumeric(?o)).
        }
"""

QU6 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:time ?t.
            ?e mimic:u1 ?u1.
            ?e mimic:u2 ?u2.
            ?e mimic:rt ?rt.
            ?e mimic:m1 ?m. 
            ?e mimic:v1 ?o.
            ?e mimic:m2 ?m2.
            ?e mimic:v2 ?o2.
            FILTER(isNumeric(?o2) && isNumeric(?o)).
            MINUS {?s foaf:name "%s"}
        }


"""

##########################################
## ONE TRIPLE MATCHED

Q7 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:time "2682-09-12 20:00:00 -0500".
            ?e mimic:v1 ?o.            
            FILTER(isNumeric(?o)).
        }
"""

QU7 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:time "2682-09-12 20:00:00 -0500".
            ?e mimic:v1 ?o.            
            FILTER(isNumeric(?o)).
            MINUS {?s foaf:name "%s"}
        }


"""


##########################################
## NO TRIPLES MATCHED

Q8 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:time "FAKE TIME".
            ?e mimic:v1 ?o.            
            FILTER(isNumeric(?o)).
        }
"""

QU8 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:time "FAKE TIME".
            ?e mimic:v1 ?o.            
            FILTER(isNumeric(?o)).
            MINUS {?s foaf:name "%s"}
        }


"""

################################################
## TEST TWO FUNCTIONS AT ONCE
## It is important that the second operation be put second
## Only one triple should match

Q9 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

SELECT (%s(?o) as ?aggr) (COUNT(?o2) as ?other)  WHERE{
    ?s foaf:name ?n.
    ?s mimic:event ?e.
    ?e mimic:time "2682-09-12 20:00:00 -0500".
    ?e mimic:v1 ?o.
    ?e mimic:v2 ?o2.
    FILTER(isNumeric(?o2) && isNumeric(?o)).
}
"""

QU9 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

SELECT (%s(?o) as ?aggr) (COUNT(?o2) as ?other) WHERE{
    ?s foaf:name ?n.
    ?s mimic:event ?e.
    ?e mimic:time "2682-09-12 20:00:00 -0500".
    ?e mimic:v1 ?o.            
    ?e mimic:v2 ?o2.
    FILTER(isNumeric(?o2) && isNumeric(?o)).
    MINUS {?s foaf:name "%s"}
}


"""


################################################
## ANOTHER TEST TWO FUNCTIONS AT ONCE
## It is important that the second operation be put second
## More than one triple should match


Q10 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 "Insulin".
            ?e mimic:v1 ?o.
            ?e mimic:v2 ?o2.
            FILTER(isNumeric(?o)).
            FILTER(?o > 1)
        }
"""

QU10 = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1#>
PREFIX mimic: <http://air.csail.mit.edu/spim_ontologies/mimicOntology#>

        SELECT (%s(?o) as ?aggr) WHERE{
            ?s foaf:name ?n.
            ?s mimic:event ?e.
            ?e mimic:m1 "Insulin".
            ?e mimic:v1 ?o.
            ?e2 mimic:v2 ?o2.
            FILTER(isNumeric(?o)).
            FILTER(?o > 1)
            MINUS {?s foaf:name "%s"}
        }
"""


