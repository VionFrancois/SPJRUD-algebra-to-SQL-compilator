import syntax
from SyntaxTree import *

FIRST_ATTRIBUTE = "attributeONE"
SECOND_ATTRIBUTE = "attributeTWO"
FIRST_RELATION = "relation_ONE"
SECOND_RELATION = "relation_TWO"
CONSTANT = "constant" 
OPERATOR_EQ = "="
OPERATOR_DIF = "!="

#test 1
def regex_test():
    assert syntax.syntax_is_correct(syntax.remove_space(f"Select({FIRST_ATTRIBUTE}, {OPERATOR_DIF}, {CONSTANT}, {FIRST_RELATION})"))
    assert syntax.syntax_is_correct(syntax.remove_space(f"Project([{FIRST_ATTRIBUTE},{SECOND_ATTRIBUTE}], {FIRST_RELATION})"))
    assert syntax.syntax_is_correct(syntax.remove_space(f"Join({FIRST_RELATION}, {SECOND_RELATION})"))
    assert syntax.syntax_is_correct(syntax.remove_space(f"Rename({FIRST_ATTRIBUTE}, {CONSTANT},{FIRST_RELATION})"))
    assert syntax.syntax_is_correct(syntax.remove_space(f"Union({FIRST_RELATION}, {SECOND_RELATION})"))
    assert syntax.syntax_is_correct(syntax.remove_space(f"Difference({FIRST_RELATION}, {SECOND_RELATION})"))
    assert syntax.syntax_is_correct(syntax.remove_space(f"Project([*], {FIRST_RELATION})"))
    assert syntax.syntax_is_correct(syntax.remove_space(f"Select({FIRST_ATTRIBUTE}, {OPERATOR_DIF}, {CONSTANT}, Join(Join({FIRST_RELATION},{SECOND_RELATION}), Union({FIRST_RELATION}, {SECOND_RELATION})))"))
    print("Test one passed.")

#test 2
def check_error():
    assert syntax.syntax_is_correct(syntax.remove_space(f"PROJECT({FIRST_ATTRIBUTE}, {FIRST_RELATION})")) == False
    assert syntax.syntax_is_correct(syntax.remove_space(f"Join({FIRST_RELATION}, {SECOND_RELATION}, re3)")) == False
    assert syntax.syntax_is_correct(syntax.remove_space(f"Project([{FIRST_ATTRIBUTE}, {SECOND_ATTRIBUTE}], {FIRST_RELATION}")) == False
    assert syntax.syntax_is_correct(syntax.remove_space(f"Select({FIRST_ATTRIBUTE}, !==, {CONSTANT}, {FIRST_RELATION})")) == False
    assert syntax.syntax_is_correct(syntax.remove_space(f"Select({FIRST_ATTRIBUTE}, {OPERATOR_DIF}, {CONSTANT}, Join(Join({FIRST_RELATION},{SECOND_RELATION}), error({FIRST_RELATION}, {SECOND_RELATION})))")) == False
    print("Test two passed.")

def request():
    db = DataBase("test.db")
    # Select
    assert SyntaxTree.convertToSQL(SyntaxTree("Select(first_name,=,julien,contacts)",db).root,db)[0] == "SELECT * FROM (contacts) WHERE first_name = 'julien'"
    # Project
    assert SyntaxTree.convertToSQL(SyntaxTree("Project([first_name,contact_id],contacts)",db).root,db)[0] == "SELECT first_name, contact_id FROM (contacts)"
    # Join
    assert SyntaxTree.convertToSQL(SyntaxTree("Join(cities,contacts)",db).root,db)[0] == "SELECT * FROM (contacts) NATURAL JOIN (cities)"
    # Rename
    assert SyntaxTree.convertToSQL(SyntaxTree("Rename(Country,Pays,cities)",db).root,db)[0] == "SELECT Country AS 'Pays' FROM (cities)"
    # Union
    assert SyntaxTree.convertToSQL(SyntaxTree("Union(cities,cities)",db).root,db)[0] == "SELECT * FROM (cities) UNION SELECT * FROM (cities)"
    # Difference
    assert SyntaxTree.convertToSQL(SyntaxTree("Difference(cities,cities)",db).root,db)[0] == "SELECT * FROM (cities) EXCEPT SELECT * FROM (cities)"
    # Combiné
    assert SyntaxTree.convertToSQL(SyntaxTree("Select(firstName,=,julien,Project([firstName],Rename(first_name,firstName,Join(cities,contacts))))",db).root,db)[0] == "SELECT * FROM (SELECT firstName FROM (SELECT first_name AS 'firstName' FROM (SELECT * FROM (contacts) NATURAL JOIN (cities)))) WHERE firstName = 'julien'"

    print("Test three passed")
        

'''
Test unitaires 
'''
if __name__ == "__main__":
    # regex_test()
    # check_error()
    request()
