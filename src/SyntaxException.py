import re

SELECT = r"Select\(Att\([a-zA-Z0-9\(\),]+\),((=)|(!=)),Re\([a-zA-Z0-9\(\),]+\)\)"
PROJECT = r"Project\(Att\([a-zA-Z0-9\(\),]+\),Re\([a-zA-Z0-9\(\),]+\)\)"
JOIN = r"Join\(Rel\([a-zA-Z0-9\(\),]+\),Re\([a-zA-Z0-9\(\),]+\)\)"
RENAME = r"Rename\(Att\([a-zA-Z0-9\(\),]+\),Cst\([a-zA-Z0-9^\0]+\),Re\([a-zA-Z0-9\(\),]+\)\)"
UNION = r"Union\(Rel\([a-zA-Z0-9\(\),]+\),Re\([a-zA-Z0-9\(\),]+\)\)"
DIFFERENCE = r"Difference\(Rel\([a-zA-Z0-9\(\),]+\),Re\([a-zA-Z0-9\(\),]+\)\)"


def remove_space(s):
    res = ""
    for i in s:
        if(i != " "):
            res += i
    return res
     
assert re.match(SELECT, remove_space("Select(Att(Country) ,= , Re(Mali))"))
    

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


l = "Select(Country , =, Mali , CC )"
print(split('(', ',', ')', l))

