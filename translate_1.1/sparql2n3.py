## File to to translate sparql to n3. Uses Rasqal library's roqet function.
## VERY DIFFERENT from the sparql2n3.py file written for iarpa-pir policy-awareness project.
## However, the ontology used is just an extended version of the iarpa one, just to make it compatible
## with previous AIR policies.

import os
import subprocess

#Set here to have a trace printed
debug = False

#Set the header for the n3 file outputted here
header = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix s: <http://air.csail.mit.edu/spim/sparql_1.1.n3>.

@prefix : <http://air.csail.mit.edu/spim/translation_output.n3>. """

def dprint(string):
	if debug:
		print string

#Class to build parsed tree
class ExpressionTreeBuilder:

	def __init__(self):
		pass

	def translateSparqlToN3(self, query):
		self.initialBuild(query)
		self.parseVerbClause()
		self.parseVarClause()
		self.parsePatternTree()
		print self.initialTree.other_unparsed
		
		self.translateToN3()

	def initialBuild(self, query):
		splitQuery = query.split('\n')
		clauseTree = StructureSplitter()
		print "########################"
		print splitQuery
		print "########################"
		for i in range(len(splitQuery)):
			if 'query Group graph pattern' in splitQuery[i]:
				clauseTree.query_patterns_unparsed += [splitQuery[i:]]
				break
			elif 'query bound variables' in splitQuery[i]:
				clauseTree.query_varList_unparsed += [splitQuery[i]]
			elif 'query verb' in splitQuery[i]:
				clauseTree.query_verb_unparsed += [splitQuery[i]]
			else:
				clauseTree.other_unparsed += [splitQuery[i]]
		print "TREE CONSTRUCTED"
		self.initialTree = clauseTree	
		return True

	def parseOther(self):
		pass

	#Parses the verb split from the initial structure
	def parseVerbClause(self):
		self.query_verb = self.initialTree.query_verb_unparsed[0][12:]
		print self.query_verb, " is query verb"

	def parseVarClause(self):
		print "@@@@@@@@   PARSING VARS" 
		vars = self.initialTree.query_varList_unparsed
		vars = vars[0].split(':')[1]
		self.vars = vars.split(',')
		print vars

		#Make a clause structure if needed
		for i in range(len(self.vars)):
			if '=' in self.vars[i]: #There is a "var1 as var2" clause
				asASplit = self.vars[i].split('=') 
				#Ignore the name of the variable returned, since we only care about the variable
				#originally bound
				clause = createClause(self.vars[i], '(', ')')
				print clause
				self.vars[i] = clause
			#Else: Variable is returned as-is, so no change.
			else:
				self.vars[i] = Pattern([self.vars[i]], "variable") 


	def parsePatternTree(self):
		print self.initialTree.query_patterns_unparsed
		for main_graph_pattern in self.initialTree.query_patterns_unparsed:
			fullPattern = ''
			for string in main_graph_pattern:
				fullPattern += string
			print "############################"
			print fullPattern

		self.graph_patterns = createClause(fullPattern)
		print self.graph_patterns

	#Uses the data structure built by the parse functions above to construct the tree
	def translateToN3(self):

		#Get the state for purposes of naming the queries.
		f = open("state.txt")
		counter = int(f.readline())
		f.close()
		f = open("state.txt", "w")
		f.write(str(counter + 1))
		f.close()

		#Start by naming query and what type it is
		output_file = open("query_in_n3.n3", "w")
		output_file.write(header)
		output_file.write("\n\n:Query" + str(counter) + " a s:SPARQLQuery;") 
		output_file.write("\n\t a s:" + self.query_verb.lower() + "_query;")
		
		#Next, we output the variables retrieved.
		output_file.write("\ns:retrieve [")
		for s in self.vars:
			continue
			output_file.write(s.toN3())	
		output_file.write("\n];")
						
	
##########################################
#Quite stupid. Scan string looking for curly bracers, until you find one. Then scan the rest of the screen to find
#the subclauses and creates them recursively. All in all takes O(n^2) time and space, but considering SPARQL 
#queries are not too large this should not be too much of a problem.

def createClause(string, left_brace = '{', right_brace = '}'):	

	counter_string = 0
	length = len(string)
	counter_num_right_brace = 0
	counter_num_left_brace = 0
	
	dprint("%%%%%%%%%%%%%%%%%%%%%%%%")
	dprint("STRING = " + string)

	#Find first curly brace
	while counter_string < length:
		if string[counter_string] == left_brace:
			counter_num_left_brace += 1
			break
		counter_string += 1

	#If we meet this next condition, one of two things are possible. Most likely, we have reached the end of
	#the recursion, which means that we must build the triple, operation, or expression clause. Otherwise,
	#there is an error, and something is very very wrong.

	if counter_num_left_brace == 0:
		if right_brace in string: #Unbalanced expression
			print "Unbalanced curly braces. Error!"
			return EmptyClause()
		elif left_brace == '(' and right_brace ==')':
			dprint("Reached name or literal!")
			return string

		#Do this now with parantheses instead of bracers
		return createClause(string, '(', ')')
	
				
	
	#Continue on with curly bracer finding

	#Find keyword of the expression (e.g. basic_graph_pattern), which will be the token
	keyword = string[0:counter_string]
	keyword = keyword.replace(' ', '')
	dprint("KEYWORD = " + keyword)
	if keyword == "triple":
		vars = string[(counter_string+1):].split(',')
		all_clauses = [createClause(s, '(', ')') for s in vars]
		return Pattern(all_clauses, "triple")	

	#Take care of expression clauses by parsing using parantheses
	elif keyword == "expr":
		return Pattern([createClause(string[counter_string:], '(', ')')], "expr")

	#Take care of variables and literals
	elif keyword == "variable" or keyword == "string" or keyword == "integer" or keyword == "float":
		return Variable([string[counter_string:]], keyword)

	#Need to make a clause out of every sub-expression enclosed in curly bracers.
	#The invariant: We always have one left curly open. When we have zero open, then we have finished the 
	#current expression.

	list_subclauses = []
	pos_first_left_curly = counter_string

	while counter_string < length:
		c = string[counter_string]
		if c == left_brace:
			counter_num_left_brace += 1
			if counter_num_left_brace == 2: #Just opened a new subclause to be built
				pos_first_left_curly = counter_string + 1
		elif c == right_brace:
			counter_num_left_brace -= 1
			if counter_num_left_brace == 1:
			#At this point, we have closed one round of subexpression, so make a clause out of it.
			#e.g. in subgraph { triples { ... } triples {...} }, we will have read all the first
			#triples clause when the balance of open curly braces is one.

				#Save indices of the string which define a subclause
				list_subclauses += [(pos_first_left_curly, counter_string)] 
		counter_string += 1	

		
	list_built_clauses = []

	#Build the subclauses from the indices
	if len(list_subclauses) > 0:
		dprint("We have the following subclauses")
		dprint([string[i:j] for i, j in list_subclauses])
		#Bit of a hack, b	
		for i in list_subclauses:
			b, e = i[0], i[1]
			newString = string[b:e]
			list_built_clauses += [createClause(newString)]
				
		return Pattern(list_built_clauses, keyword)

	#If we reached this point, curly bracers were unbalanced. Error
	print "Error: Unbalanced curlies"
	return EmptyClause()	


###########################################
#Initial class to build parsed tree
class StructureSplitter:
	
	def __init__(self, query_verb = [], query_varList = [], query_patterns = [], other = []):
		self.query_verb_unparsed = query_verb
		self.query_varList_unparsed = query_varList
		self.query_patterns_unparsed = query_patterns
		self.other_unparsed = other

	def __str__(self):
		return str(self.query_verb) + '\n\n' + str(self.query_varList) + '\n\n' + str(self.query_patterns) + '\n\n' + str(self.other) 

########################################
#Virtual class to make everything standarized
class Clause:

	def __init__(self):
		self.token = "Virtual"
		self.nested_clauses = []

	def toN3(self):
		pass

	def __str__(self):
		toPrint = self.token + ' [ ' 
		for i in self.nested_clauses:
			toPrint += str(i)
		toPrint = toPrint + ' ] '
		return toPrint
########################################
#To avoid null problems
class EmptyClause(Clause):
	
	def __init__(self):
		self.token = "Empty"

	def toN3(self):
		print "Error! This clause identifies an error in the parsing. Make sure code is correct"
		raise Exception("Error! This clause identifies an error in the parsing. Make sure the code is correct")


########################################
class Pattern(Clause):
	
	#A clause. The types of tokens supported: unknown, basic_graph_pattern, sub_graph_pattern, 
	#filter, op_(OP NAME IN LOWERCASE), triples_clause, expression, triple, variable, string_literal, etc.
 	#Note that for the purposes of simplicity, variables and literals are also treated as clause objects. The 
	#name of these will be put in the nested_clauses subvariable (e.g. self.nested_clauses = ['x']).
	def __init__(self, nested_clauses, token = "Unknown"):
		self.nested_clauses = nested_clauses
		self.token = token

	def toN3(self):
		return "\ns:" + token
	
#########################################

class Variable(Clause):
	#Inherets from clause for convinience. Encompasses both literals and variables
	
	#For convinience, varname (also the literal name must be in list form (e.g. ["'Charlie'"] or ['x'])
	def __init__(self, varName, token):
		self.nested_clauses = varName #Called nested_clauses to match the clause class only.
		self.token = token


def translate(query):
	##Part 1: Send sparql query through roqet
	command = "roqet -i sparql -d structure -n -e " + query
	#os.system(command)
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
	output = process.communicate()[0]
	print output


	builder = ExpressionTreeBuilder()
	builder.translateSparqlToN3(output)

def main():
	sample_query = """'
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT DISTINCT ?x (?b as ?name) (AVG(?x) as ?y) 
WHERE{ ?a foaf:age ?x; foaf:name ?b; <http://example.com#hasFriend> [ foaf:name ?name]. FILTER(isNumeric(?x)) FILTER(?x > "10").} GROUP BY ?x' """
	translate(sample_query)

if __name__ == "__main__":
	main()
