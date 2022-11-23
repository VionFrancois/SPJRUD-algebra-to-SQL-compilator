import re

CONSTANT = r"Cst\([a-zA-Z0-9\(\),]+\)"
ATTRIBUTE = r"Att\([a-zA-Z0-9\(\),]+\)"
RELATION = r"Re\([a-zA-Z0-9\(\),]+\)"

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
    sub_parenthesis = False
    for i in range(0, len(s)):
        if(s[i] == '('):
            sub_parenthesis = True
        elif(s[i] == ')' and sub_parenthesis):
            sub_parenthesis = False
        elif(s[i] == ')'):
            return i

def is_there_enough_parenthesis(s):
    parenthesis = 0
    for i in s:
        if(i == '(' or i == ')'):
            parenthesis += 1
    return parenthesis % 2 == 0

def search_under_request(s):
    parenthesis = [i for i in s if i == '(' or i == ')']
    count_opened_parenthesis = 0
    for i in range(0, len(parenthesis)):
        if(parenthesis[i] == '('):
            count_opened_parenthesis +=1
        if(count_opened_parenthesis >= 3):
            return i
        elif(parenthesis[i] == ')'):
            count_opened_parenthesis = 0
    return -1

    
def check_syntax(s):
    try:

        print(s)
        answer = False
        for i in SPJRUD_REGEX:
            if(re.match(i, s) != None):
                answer = True
                break
        
        assert answer, f"Syntax error, the part '{s}' is wrong"
        begin_of_the_request = search_under_request(s)
        print(begin_of_the_request)
        if begin_of_the_request != -1:
            closed_indice = find_closed_parenthesis(s[begin_of_the_request:])
            assert closed_indice != -1, f"your parenthesis are not well managed"
            answer = check_syntax(s[i + 1: closed_indice + i])                
        return answer
    except AssertionError as e:
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


l = "Select(Att(Country),=,Cst(Mali),Re(CC))"
#print(re.match(SELECT, l))
#print(check_syntax(remove_space(l))) #vrai
#l = "Select(Att(country), egual, att(Mali), Re(CC))"
#print(check_syntax(remove_space(l))) #faux
l = "Select(Att(country), =, Cst(b), Re(Join(Re(R1), Re(R2))))"
print(check_syntax(remove_space(l))) #vrai
l = "Project(Att(1), Re(Union(Re(un), Rel(deux))))"
#print(check_syntax(remove_space(l))) #vrai




