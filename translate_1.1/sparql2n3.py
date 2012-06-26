## File to to translate sparql to n3. Uses Rasqal library's roqet function.
## VERY DIFFERENT from the sparql2n3.py file written for iarpa-pir policy-awareness project.
## However, the ontology used is just an extended version of the iarpa one, just to make it compatible
## with previous AIR policies.

import os
import subprocess
import re

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
		print vars, ", VARS"
		retrieved_expressions = []

		#Make a clause structure if needed
		for i in range(len(self.vars)):
			if '=' in self.vars[i]: #There is a "var1 as var2" clause
				asASplit = self.vars[i].split('=') 
				
				#Remember name of the variable, and create a condition clause on the "as a"
				#clause

				self.vars[i] = Variable(asASplit[0], "variable")	
				clause = createClause(asASplit[1], '(', ')')
				print clause
				retrieved_expressions += [Binding([self.vars[i], clause], "binding")]
				#self.retrieved_expressions[asASplit[0]] = clause
			#Else: Variable is returned as-is, so no change.
			else:
				print "VARNAME", self.vars[i]	
				self.vars[i] = Variable(self.vars[i], "variable") 

		#Finally, make the retrieved expression a single clause object
		self.retrieved_expressions = Pattern(retrieved_expressions, "retrieved_expressions")

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

		output_file.write("\n\ts:retrieve [")
		for r in self.vars:
			output_file.write("\n\t\t s:var " + r.toN3() + ';')	
		output_file.write("\n\t];")

		#Next, make clauses for retrieved variables

		output_file.write("\n\ts:clause [")

		#First, go through the clauses from the retrieve section
		for c in self.retrieved_expressions.nested_clauses:
			output_file.write(c.toN3(2))						
#		output_file.write(self.retrieved_expressions.toN3(1))
		output_file.write('\n')	
	
		#Now go through the other clauses
		output_file.write(self.graph_patterns.toN3(2))
		output_file.write("\t];")

	
##########################################
#Quite stupid. Scan string looking for curly bracers, until you find one. Then scan the rest of the screen to find
#the subclauses and creates them recursively. All in all takes O(n^2) time and space, but considering SPARQL 
#queries are not too large this should not be too much of a problem.

def createClause(string, left_brace = '{', right_brace = '}'):	

#	print "STRING, ", string

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
			return Variable(string, "string")

		#Do this now with parantheses instead of bracers
		return createClause(string, '(', ')')
	
				
	
	#Continue on with curly bracer finding

	#Find keyword of the expression (e.g. basic_graph_pattern), which will be the token
	keyword = string[0:counter_string]

	#Look for op keywords before doing regex processing
	matching = re.match('op [\w]+', keyword)
	if matching != None:
		print keyword, "IS IT OP?"
		a, b = counter_string + 1, len(string) - 1 #These indices help get rid of extra parantheses
		newString = string[a:b]
		print newString
		separated = newString.split(',')
		return Operation([createClause(s, '(', ')') for s in separated], keyword.replace(' ', '_'))

	#Some regex processing to make keyword better


	keyword = keyword.replace(' ', '')
#	keyword = re.sub("[^\w]\d+[\w]*", '', keyword)

#	if keyword == '':
#		print "BLANK", counter_string
#		return createClause(string[counter_string:])

	if keyword == "triple":
		vars = string[(counter_string+1):].split(',')
		three_vars = [createClause(s, '(', ')') for s in vars]
		return Triple(three_vars, "triple")	

	#Take care of expression clauses by parsing using parantheses
	elif keyword == "expr":
		return Pattern([createClause(string[counter_string:], '(', ')')], "expr")

	#Take care of variables and literals
	elif keyword == "variable" or keyword == "string" or keyword == "integer" or keyword == "float":
		return Variable(string[counter_string:], keyword)

	elif keyword == "filter":
		return Filter([createClause(string[counter_string:])], 'filter')	

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

	#Depth is used to make the tab characters
	def toN3(self, depth = 0):
		pass

	def __str__(self):
		toPrint = self.token + ' [ ' 
		for i in self.nested_clauses:
			toPrint += str(i)
		toPrint = toPrint + ' ] '
		return toPrint

	def sub_var_clauses(self):
		pass	


########################################
#To avoid null problems
class EmptyClause(Clause):
	
	def __init__(self):
		self.token = "Empty"

	def toN3(self, depth = 0):
		print "Error! This clause identifies an error in the parsing. Make sure code is correct"
		raise Exception("Error! This clause identifies an error in the parsing. Make sure the code is correct")

	def sub_var_clauses(self):
		return None

########################################
class Pattern(Clause):
	
	#A general clause. The types of tokens supported: unknown, basic_graph_pattern, sub_graph_pattern, 
	#filter, op_(OP NAME IN LOWERCASE), triples_clause, expression, triple, variable, string_literal, etc.
 	#Note that for the purposes of simplicity, variables and literals are also treated as clause objects. The 
	#name of these will be put in the nested_clauses subvariable (e.g. self.nested_clauses = ['x']).

	def __init__(self, nested_clauses, token = "Unknown"):
		self.nested_clauses = nested_clauses
		self.token = token

	#This version, skip the pattern keyword and just go down to where there is a triple pattern
	def toN3(self, depth = 0):
		toReturn = ''

		#Special case: Operations will be slightly more difficult
#		if self.keyword == "op":
			

		for s in self.nested_clauses:
			toReturn += s.toN3(depth)
		return toReturn

	#Function not in use anymore
	def toN3_old(self, depth = 0):

		print "TOKEN IS", self.token, " AND ", self.nested_clauses
		newStr = "__" + self.token + "__"
		print newStr
		#Deal with blanks first
		if self.token == '':
			toReturn = ''
			for s in self.nested_clauses:
				toReturn += s.toN3(depth)
			return toReturn 
		
		if self.token != '':
			toReturn = "\n" + '\t'*depth + "[ s:" + self.token
		else:
			toReturn = ''
		#toReturn += '[ '
		for i in range(len(self.nested_clauses)):
			toReturn += self.nested_clauses[i].toN3(depth + 1)
			if i == len(self.nested_clauses) - 1:
				toReturn += '\n' + '\t'*(depth) + '].'
			else:
				toReturn += '\n' + '\t'*(depth) + '];'
		return toReturn
	
	def sub_var_clauses(self):
		toReturn = []
		for s in self.nested_clauses:
			toReturn += s.sub_var_clauses()
		return toReturn

########################################
class Filter(Clause):

	def __init__(self, nested_clauses, token):
		self.nested_clauses = nested_clauses
		self.token = token

	#Slightly hacked by looking into next clause in series. Fix if possible
	def toN3(self, depth = 0):
		if len(self.nested_clauses) > 1:
			print "LONGER LENGTH, ", len(self.nested_clauses)
		subclause = self.nested_clauses[0]
		if subclause.token[0:1] == 'op':
			print subclause.token, "SUBCLAUSE"

		toReturn = ''
		toReturn = '\t'*depth + "s:filter "
		for c in self.nested_clauses:
			toReturn += c.toN3() + ';\n'	
		return toReturn

########################################
#Right now, operation objects only handle functions of one or two input variables
class Operation(Clause):

	def __init__(self, nested_clauses, token):
		self.nested_clauses = nested_clauses
		self.token = token

	def toN3(self, depth = 0):
		print "OP", self.token, len(self.nested_clauses)
		print self.nested_clauses
		toReturn = ''
		if len(self.nested_clauses) == 2:
			toReturn += '\t'*depth + '{'
			toReturn += self.nested_clauses[0].toN3() + " s:" + self.token + " "
			toReturn += self.nested_clauses[1].toN3() + '}'
	
		elif len(self.nested_clauses) == 1:
			toReturn += ' [ s:' + self.token + ' ' + self.nested_clauses[0].toN3() + ']' 
		else:
			toReturn = " CANNOT HANDLE THIS MANY INPUT VARS FOR THIS OP"
		
		return toReturn
		


#########################################

class Variable(Clause):
	#Inherets from clause for convinience. Encompasses both literals and variables
	
	#For convinience, varname (also the literal name must be in list form (e.g. ["'Charlie'"] or ['x'])
	#Also, token is just 
	def __init__(self, varName, token):
		newVar = varName.replace(" ", "")
		newVar = newVar.replace("(", "")
		newVar = newVar.replace(")", "")
		self.nested_clauses = [newVar] #Called nested_clauses to match the clause class only.
		self.token = token

	def toN3(self, depth = 0):
		print "VARIABLE TOKEN IS,", self.token
		if self.token == "variable":
			return " :" + self.nested_clauses[0]  
		else:
			return self.nested_clauses[0]


	def sub_var_clauses(self):
		return [self]

##########################################

class Triple(Clause):
	
	def __init__(self, triple_of_vars, token):
		self.nested_clauses = triple_of_vars
		self.token = token

	def toN3(self, depth = 0):
		print "TRIPLE", self.nested_clauses
		toReturn = '\t'*depth + "s:triplePattern { "
		for var in self.nested_clauses:
			toReturn += var.toN3() + " "
		return toReturn + "};\n"

##########################################

class Binding(Clause):
		
	def __init__(self, two_clauses, token):
		self.nested_clauses = two_clauses
		self.token = token

	def toN3(self, depth=0):
		toReturn = '\n' + '\t'*depth + 's:triplePattern { '
		toReturn += self.nested_clauses[0].toN3(depth+1) + " s:bound_as " + self.nested_clauses[1].toN3(depth + 1) + "};"		
		return toReturn #+ '.\n'
##########################################

class Expression(Clause):

	def __init__(self, nested_clauses, token = "Expression"):
		self.nested_clauses = nested_clauses
		self.token = token

	def toN3(self, depth = 0):
		toReturn = '\n' + '\t'*depth + " s:expression"

##########################################

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
WHERE{ ?a foaf:age ?x; foaf:name ?b; <http://example.com#hasFriend> [ foaf:name ?friend_name]. FILTER(isNumeric(?x)) FILTER(?x > "10").} GROUP BY ?x' """
	translate(sample_query)

if __name__ == "__main__":
	main()
