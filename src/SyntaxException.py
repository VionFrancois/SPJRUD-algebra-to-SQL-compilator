import re

CONSTANT = r"Cst\([a-zA-Z0-9]+\)"
ATTRIBUTE = r"Att\([a-zA-Z0-9]+\)"
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
    return -1

def is_there_enough_parenthesis(s):
    parenthesis = 0
    for i in s:
        if(i == '('):
            parenthesis += 1
        elif(i == ')'):
            parenthesis -= 1
        
    return parenthesis == 0

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
        assert is_there_enough_parenthesis(s), f"some of your parenthesis are not closed"
        print(s)
        answer = False
        for i in SPJRUD_REGEX:
            if(re.match(i, s) != None):
                answer = True
                break
        
        assert answer, f"Syntax error, the part '{s}' is wrong"
        begin_of_the_request = search_under_request(s)
        if begin_of_the_request != -1:
            closed_indice = find_closed_parenthesis(s[begin_of_the_request:])
            under_request = s[begin_of_the_request + 1: closed_indice + begin_of_the_request + 1]
            answer = check_syntax(under_request)                
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
print(re.match(SELECT, l))
print(check_syntax(remove_space(l))) #vrai
l = "Select(Att(country), egual, att(Mali), Re(CC))"
print(check_syntax(remove_space(l))) #faux
l = "Select(Att(country), =, Cst(b))), Re(Join(Re(R1), Re(R2))))"
print(check_syntax(remove_space(l))) #faux
l = "Project(Att(1), Re(Union(Re(un), Re(deux))"
print(check_syntax(remove_space(l))) #faux
l = "Project(Att(Project(Att(1),Re(Join(Re(2), Re(3), Re(4))"
print(check_syntax(remove_space(l)))




