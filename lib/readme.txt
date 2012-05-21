This document will give a short description of what the different files contain. 

1) spim.py
The central file for the project that manages how queries are carried out and whether a query complies with the given set of policies. A spim object is created that is used to communicate with the given SPARQL endpoint. The main method, acceptQuery, accepts a query and carries out all the required policy checking and differential privacy updates necessary.
