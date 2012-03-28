#!/usr/bin/python

import sys
import cgi
sys.path.append('lib/')
import endpoint
from spim import SPIM
from pprint import pprint


def generate_site(results = ""):
	
	print "<html>\n<head> \n<title>Spim Online Demo </title>\n</head>"
	print "<body>\n"
	print "<p>Please enter your desired query here</p>"
	print "<form method='post' name='form1'>"
	print """<textarea rows='20' cols='70' name='query'>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT (COUNT(?p) as ?size) WHERE {
	?s ?p ?o
} LIMIT 1000
	 </textarea>\n"""

	print "<br /> Username: <input type='text' name='username' /> <br />"
	print "<input type='submit' value='enter'></input>\n"
	print "</form>"


def main():

	endpoint_address = "http://air.csail.mit.edu:83"
	spimThread = SPIM(endpoint_address, '4store')
	form = cgi.FieldStorage()
	print "Content-Type: text/html\n\n"
	generate_site()
	endpoint = "http://air.csail.mit.edu:81"

	#Methods when query is received
	if form.has_key("query"):
		print "\n\nYou have entered in the following query:<br><br>"
		print str(form["query"].value)
		print "<br><br>"

		if not form.has_key("username"):
			username = "user0"
		else:
			username = form['username'].value

		#Sending the result to the spim module
		print "The result is:<br>"
		result = spimThread.acceptQuery(form['query'].value, username)
		pprint(result)

	
	print "</body>\n</html>"


if __name__ == "__main__":
	main()	
