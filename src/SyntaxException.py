import re

CONSTANT = r"[a-zA-Z0-9]+"
ATTRIBUTE = CONSTANT
RELATION = r"[a-zA-Z0-9\(\),]+"

SELECT = r"Select\("+ ATTRIBUTE +r",((=)|(!=))," + CONSTANT + r","+ RELATION + r"\)"
PROJECT = r"Project\("+ ATTRIBUTE +r"," + RELATION + r"\)"
JOIN = r"Join\(" + RELATION + r","+ RELATION + r"\)"
RENAME = r"Rename\(" + ATTRIBUTE +r"," + CONSTANT +r"," + RELATION+ r"\)"
UNION = r"Union\("+ RELATION+r"," + RELATION + r"\)"
DIFFERENCE = r"Difference\("+ RELATION + r","+ RELATION +r"\)"

SPJRUD_REGEX = [SELECT, PROJECT, JOIN, RENAME, UNION, DIFFERENCE]
SPJRUD = ["Select", "Project", "Join", "Rename", "Union", "Difference"]

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

    
def check_syntax(s):
    try:
        is_closed, last_parenthesis = is_there_enough_parenthesis(s)
        if(is_closed < 0):
            raise Exception(f"there is too many parenthesis:\n{s}\n"+ " "*(last_parenthesis) +"^")
        elif(is_closed > 0):
            raise Exception(f"the parenthesis at index {last_parenthesis} is not closed:\n{s}\n" + " "*(last_parenthesis) + "^")
        answer = False
        for i in SPJRUD_REGEX:
            if(re.match(i, s) != None):
                answer = True
                break

        if(not answer):
            raise Exception(f"Syntax error, the part '{s}' is wrong")

        begin_of_the_request = search_under_request(s)
        if begin_of_the_request != -1:
            closed_indice = find_closed_parenthesis(s[begin_of_the_request:])
            under_request = s[begin_of_the_request + 1: closed_indice + begin_of_the_request + 1]
            answer = check_syntax(under_request)                
        return answer
    except Exception as e:
        print(e)
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


l = "Select(Country,=,Mali,CC)"
print(check_syntax(remove_space(l))) #vrai
l = "Select(country, egual, Mali, CC)"
print(check_syntax(remove_space(l))) #faux
l = "Select(country, =, b, Join(R1, R2)"
print(check_syntax(remove_space(l))) #faux
l = "Project(1, Union(un, deux))"
print(check_syntax(remove_space(l))) #faux
l = "Project(Project(1,Join(2, 3, 4)))" #faux
print(check_syntax(remove_space(l)))
l = "Select(id, =, b, Join(b, c))"
print(check_syntax(remove_space(l)))





