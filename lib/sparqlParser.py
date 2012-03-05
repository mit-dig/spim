#Does not yet verify SPARQL queries are written correctly.

import re
import string

selectFindA = re.compile(r'SELECT[a-zA-Z\?\(\) ]*')
#countFindA = re.compile(r'COUNT\([\?a-zA-Z ]+\)')
ExprFind = re.compile(r'\([\?a-zA-Z ]+\)')
countFind = re.compile(r'\([cC][oO][uU][nN][tT]\(\?[a-zA-Z]+\) [aA][sS] \?[a-zA-Z]+\)')
sumFind = re.compile(r'\([sS][uU][mM]\(\?[a-zA-Z]+\) [aA][sS] \?[a-zA-Z]+\)')
avgFind = re.compile(r'\([aA][vV][gG]\(\?[a-zA-Z]+\) [aA][sS] \?[a-zA-Z]+\)')
minFind = re.compile(r'\([mM][iI][nN]\(\?[a-zA-Z]+\) [aA][sS] \?[a-zA-Z]+\)')
maxFind = re.compile(r'\([mM][aA][xX]\(\?[a-zA-Z]+\) [aA][sS] \?[a-zA-Z]+\)')


#Count COUNT, SUM, AVG, MIN, and MAX, and return dictionary with these tags
#to list of variable names.
def extractAllVars(query):
    allVars = {}
    tags = ["COUNT", "SUM", "AVG", "MIN", "MAX"]
    for t in tags:
        allVars[t] = extractVars(query, t)
    return allVars

#Will extract vars for a certain aggregate function, and return a list of
#variables that will be bound to that function.
def extractVars(query, tag = "COUNT"):

    if tag == "COUNT":
        compiler = countFind
    elif tag == "SUM":
        compiler = sumFind
    elif tag == "AVG":
        compiler = avgFind
    elif tag == "MIN":
        compiler = minFind
    elif tag == "MAX":
        compiler = maxFind
    else:
        print "Error"
        compiler = countFind
    
    allVars = compiler.findall(query)
    toReturn = []
    for v in allVars:
        terms = v[1:len(v)-1]
        terms = terms.split()
        toReturn += [terms[2][1:len(terms[2])]]
    return toReturn

#Given a query, says which variables are counts.
def extractCountVars(query):
    counts = countFind.findall(query)
    toReturn = []
    for count in counts:
        terms = count[1:len(count)-1] #Remove parantheses
        print terms
        terms = terms.split() #group terms
        toReturn += [terms[2][1:len(terms[2])]] #add name of final term to counts
    return toReturn
        

def extractSumVars(query):
    sums = sumFind.findall(query)
    toReturn = []
    for s in sums:
        terms = s[1:len(s) - 1]

#
def extractCount(query):
    select = extractSelect(query)
    countVars = countFindA.findall(query) #Find number counts
    toReturn = []
    for var in countVars:
        #iterate over variables that should be counted
        newVar = ExprFind.search(var).group() #Remove 'COUNT'
        toReturn += [newVar[2:len(newVar)-1]]
    #newQ = replaceCount(query)
    return toReturn

#Extracts the select statement from the query. Should only have one select statement
def extractSelect(query):
    select = selectFindA.findall(query)
    if len(select) != 1:
        print "ERROR IN SELECT EXTRACTION"
        return
    return select[0]

#Removes Count statements
def replaceCount(query):
    q = query.split()
    for i in range(len(q)):
        s = q[i]
        if "COUNT" in s:
            q[i] = s[6:len(s) - 1] #Remove count from parantheses
    return string.join(q)
                

def main():
    query = "SELECT (min(?s) as ?rand) (SUM(?P) as ?size) ?d WHERE(?P ?s ?m)"
    print extractAllVars(query)
    

if __name__ == "__main__":
    main()
