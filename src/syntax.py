import re
from spjrud import *

# Union(([a-zA-Z0-9]+)|([a-zA-Z]+\([a-z-A-Z0-9\(\),]+\)),([a-zA-Z0-9]+)|([a-zA-Z]+\([a-z-A-Z0-9\(\),]+\)))
CONSTANT = r"[a-zA-Z0-9_]+"
ATTRIBUTE = CONSTANT
ATTRIBUTES = r"[a-zA-Z0-9_*,]+"
RELATION = r"(([a-zA-Z0-9_]+)|([a-zA-Z]+\([a-z-A-Z0-9_\(\),]+\)))"

SELECT = r"Select\("+ ATTRIBUTE +r",((=)|(!=))," + CONSTANT + r","+ RELATION + r"\)"
PROJECT = r"Project\(\["+ ATTRIBUTES +r"\]," + RELATION + r"\)"
JOIN = r"Join\(" + RELATION + r","+ RELATION + r"\)"
RENAME = r"Rename\(" + ATTRIBUTE +r"," + CONSTANT +r"," + RELATION+ r"\)"
UNION = r"Union\("+ RELATION+r"," + RELATION + r"\)"
DIFFERENCE = r"Difference\("+ RELATION + r","+ RELATION +r"\)"

SPJRUD_REGEX = [SELECT, PROJECT, JOIN, RENAME, UNION, DIFFERENCE]
SPJRUD = {"Select" : Select, "Project" : Project, "Join" : Join, "Rename" : Rename, "Union" : Union, "Difference" : Difference}

def remove_space(s):
    res = ""
    for i in s:
        if(i != " "):
            res += i
    return res

def find_closed_parenthesis(s):     
    stack = []
    for i in range(0, len(s)):
        if(s[i] == '('):
            stack.append(('(', i))
        elif(s[i] == ')' and stack[-1][0] == 0):
            return i
        elif(s[i] == ')'):
            stack.pop()

def is_there_enough_parenthesis(s):
    stack = []
    for i in range(0,len(s)):
        if(s[i] == '('):
            stack.append(('(', i))
        elif(s[i] == ')'):
            if(stack != []):
                stack.pop()
            else:
                return (-1, i)
    
    if(stack == []):
        return (0,0)
        
    return (len(stack) , stack[-1][1])

def search_under_request(s):
    count_opened_parenthesis = 0
    previous_parenthesis = 0
    for i in range(0, len(s)):
        if(count_opened_parenthesis == 2 and s[i] == '('):
            return previous_parenthesis
        if(s[i] == '('):
            count_opened_parenthesis += 1
            previous_parenthesis = i
        elif(s[i] == ')'):
            count_opened_parenthesis -= 1
    return -1

    
def syntax_is_correct(s):
    try:
        is_closed, last_parenthesis = is_there_enough_parenthesis(s)
        if(is_closed < 0):
            raise Exception(f"There is too many parenthesis:\n{s}\n"+ " "*(last_parenthesis) +"^")
        elif(is_closed > 0):
            raise Exception(f"The parenthesis at index {last_parenthesis} is not closed:\n{s}\n" + " "*(last_parenthesis) + "^")
        answer = False
        for i in SPJRUD_REGEX:
            if(re.match(i, s) != None):
                answer = True
                break

        if(not answer):
            raise Exception(f"The part '{s}' is wrong.")

        begin_of_the_request = search_under_request(s)
        if begin_of_the_request != -1:
            closed_indice = find_closed_parenthesis(s[begin_of_the_request:])
            under_request = s[begin_of_the_request + 1: closed_indice + begin_of_the_request + 1]
            answer = syntax_is_correct(under_request)                
        return answer
    except Exception as e:
        print("Syntax error.", e)
        for i in SPJRUD:
            if i in s:
                print(SPJRUD[i].__doc__)
        return False

def split(delim1, delim2, forbidden,s):
    res = []
    temp = ""
    for i in range(0, len(s)):
        if(s[i] == delim1 or s[i] == delim2):
            res.append(temp)
            temp = ""
        else:
            if(s[i] != forbidden and s[i] != ' '):
                temp += s[i]
    return res

"""
l = "Select(Country,=,Mali,CC)"
print(syntax_is_correct(remove_space(l))) #vrai
l = "Select(country, egual, Mali, CC)"
print(syntax_is_correct(remove_space(l))) #faux
l = "Select(country, =, b, Join(R1, R2)"
print(syntax_is_correct(remove_space(l))) #faux
l = "Project(1, Union(un, deux))"
print(syntax_is_correct(remove_space(l))) #faux
l = "Project(Project(1,Join(2, 3, 4)))" #faux
print(syntax_is_correct(remove_space(l)))
l = "Select(id, =, b, Join(b, c))"
print(syntax_is_correct(remove_space(l)))
l = "Project(Att,Re)"
print(syntax_is_correct(remove_space(l))) #faux
l = "Project([att1,att2,att3],re1)"
print(syntax_is_correct(remove_space(l))) #vrai
l = "Join(re1, re2, re3)"
print(syntax_is_correct(remove_space(l))) #faux
"""


