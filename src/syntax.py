"""
Module vérfiant la syntaxe d'une expression SPJRUD.
"""

#utilisation des regex
import re
from spjrud import *

CONSTANT = r"[a-zA-Z0-9_]+"
ATTRIBUTE = CONSTANT
ATTRIBUTES_WITH_ALL = r"[a-zA-Z0-9_*,]+"
RELATION = r"(([a-zA-Z]+\([a-zA-Z0-9_,!=*\[\]\(\)]+)|([a-zA-Z0-9_]+))"

SELECT = r"Select\("+ ATTRIBUTE +r",((=)|(!=))," + CONSTANT + r","+ RELATION + r"\)"
PROJECT = r"Project\(\["+ ATTRIBUTES_WITH_ALL +r"\]," + RELATION + r"\)"
JOIN = r"Join\((" + RELATION + r","+ RELATION + r")\)"
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

def search_sub_request(s):
    para = s.find('(')
    sub_requests = []
    while para != -1:

        beginning_of_the_request = s[:para]

        if ',' in s[:para]:
            for i in range(para, 0, -1):
                if s[i] == ",":
                    beginning_of_the_request = s[i + 1: para]
                    break 
    
        stack = [('(', para)]
        i = para + 1
        u = 0
        while  i < len(s) and len(stack) > 0:
            if(s[i] == '('):
                stack.append(('(', i))
            elif s[i] == ')' and stack[-1][1] == para:
                u = i 
                sub_requests.append(beginning_of_the_request + s[para: i + 1])
                break
            elif s[i] == ')':
                stack.pop()
            i += 1

        para = s[u:].find('(')
        if para != -1:
            para += i
            
    return sub_requests


#On pose comme précondition que la chaine de caractère mise en argument
#ne possède aucun espace
def syntax_is_correct(s):
    try:
        is_closed, last_parenthesis = is_there_enough_parenthesis(s)
        if(is_closed < 0):
            raise Exception(f"There is too many parenthesis:\n{s}\n"+ " "*(last_parenthesis) +"^")
        elif(is_closed > 0):
            raise Exception(f"The parenthesis at index {last_parenthesis} is not closed:\n{s}\n" + " "*(last_parenthesis) + "^")
        answer = False
        for i in SPJRUD_REGEX:
            if(re.match(i, s) != None and s[::-1].find(')') == 0):

                answer = True
                break

        if(not answer):
            raise Exception(f"The part '{s}' is wrong.")

        first_paren = s.find('(')
        for sub_request in search_sub_request(s[first_paren + 1:]):
            answer = syntax_is_correct(sub_request)  

        return answer
    except Exception as e:
        print(f"Syntax error.", e)
        for i in SPJRUD:
            if i in s:
                print(SPJRUD[i].__doc__ )
        print("Type python3 main.py -h for more information.")
        return False
