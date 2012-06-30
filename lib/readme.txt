This document will give a short description of what the different files contain. 

- air-reasoner: From the policy-assurance project. The policyrunner module is used to perform access control in 
	the spim module.

- endpoint.py: Interface to speak with the HTTP4Store module for interacting with the 4store rdf data store. To
	interact with other databases, simply make a subclass of endpoint and use it.

- endpoint_ranges_gen.py: Not currently in use. Finds the min/max for each rdf:Property in 4store database. 

- endpoint_ranges.n3: Output of above script.

- func_sensitivity: 



- spim.py The central file for the project that manages how queries are carried out and whether a query complies with the given set of policies. A spim object is created that is used to communicate with the given SPARQL endpoint. The main method, acceptQuery, accepts a query and carries out all the required policy checking and differential privacy updates necessary.
