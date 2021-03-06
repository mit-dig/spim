#!/usr/bin/python

import sys
import cgi
from os import environ
sys.path.append('lib/')
import endpoint
from spim import SPIM
from pprint import pprint
import string
import Cookie


def generate_auth_site():
	print "<html>\n<head>\n<title>Spim Online Demo </title>\n</head>"
	print "<body>\nPlease input a username and password <br\>"
	print "<form method='post' name='form_auth'>"
	print """Username: <input type='text' name='username'> <br\>
	     Password: <input type='text' name='password'> <br\>
		"""
	print "<input type='submit' value='enter'></input>\n"
	print "</form>"
	print "</body></html>"

def generate_site(results = ""):
	print "<html>\n<head> \n<title>Spim Online Demo </title>\n</head>"
	print "<body>\n"
	print "<p>Please enter your desired query here</p>"
	print "<form method='post' name='form1'>"
	print """<textarea rows='20' cols='70' name='query'>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT (SUM(?o) as ?size) WHERE {
	?s ?p ?o
FILTER(isNumeric(?o))
}
	 </textarea>\n"""

	print "<br /> Username: <input type='text' name='username' /> <br />"
	print "<input type='submit' value='enter'></input>\n"
	print "</form>"


def main():

	hasUser = False
	hasPassword = False
	endpoint_address = "http://air.csail.mit.edu:81"
	spimThread = SPIM(endpoint_address, '4store', 'lib/endpoint_ranges.n3')
	form = cgi.FieldStorage()

	#Check for username/password from form and set them if necessary

#	username = "USERERROR" #this username should be replaced below. If not, error
#
#	if form.has_key("username") and form.has_key("password"):
#		cookie = Cookie.SmartCookie()
#		cookie['user'] = form['username'].value
#	    	hasUser = True
#	    	hasPassword = True
#		username = form['username'].value
#		print cookie, "\n\n"


	#check username/password from cookie
#	r_cookie = Cookie.SmartCookie(environ.get("HTTP_COOKIE", ""))

	print "Content-Type: text/html\n\n"
	
#	if environ.has_key('HTTP_COOKIE'):
#	    	for cookie in string.split(environ['HTTP_COOKIE'], ';'):
#			print cookie, "<br/>"
#			if "|" in cookie:
#				continue
#			(key, value) = string.split(cookie, '=')
#			if key == "UserID":
#		    		username = value
#		    		hasUser = True
#
#			if key == "Password":
#		    		password = value
#		    		hasPassword = True

#	if not (hasUser and hasPassword):
#	    	generate_auth_site()
#		return

	generate_site()

#	return
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
