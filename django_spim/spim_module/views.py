#Create your views here.

from django import forms
from django.shortcuts import render

import sys

sys.path.append('/var/www/spim/lib')

import spim

base_sparql_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT (SUM(?o) as ?size) WHERE {
	?s ?p ?o
	FILTER(isNumeric(?o))
}"""

class SPARQL_Query_Form(forms.Form):
	query = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows':10, 'cols':60}), initial=base_sparql_query)
	epsValue = forms.DecimalField(initial=1.0, label='Epsilon Value (Budget)')

#Class to render main page
def main(request):
	if request.method == 'POST':
		if form.is_valid():
	#		return HttpResponse('/results/')	
			return	
	form = SPARQL_Query_Form()
	return render(request, 'main.html', {'form': form,})

#Process SPARQL query using SPIM module

def results(request):

	##TODO INCLUDE SPIM CODE HERE
	new_form = SPARQL_Query_Form()
	old_form = SPARQL_Query_Form(request.POST)

	if old_form.is_valid():
		query = old_form.cleaned_data['query']
		epsValue = old_form.cleaned_data['epsValue']	
		username = 'user0'

		## SPIM INTEGRATION ##
		endpoint_address = 'http://air.csail.mit.edu:81'
		spimObject = spim.SPIM(endpoint_address, '4store', 'lib/endpoint_ranges.n3')
		spim_result = spimObject.acceptQuery(query, username)

		return render(request, 'results.html', {'form': new_form, 'query': query, 'epsValue': epsValue, 'spim_result': spim_result})

	else:
		return render(request, 'main.html')
