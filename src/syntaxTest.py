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

def global_test():
    db = DataBase("test.db")
    assert SyntaxTree.convertToSQL(SyntaxTree("Select(first_name,=,julien,contacts)",db).root,db)[0] == "SELECT * FROM contacts WHERE first_name = 'julien'"
    assert SyntaxTree.convertToSQL(SyntaxTree("Project([first_name,contact_id],contacts)",db).root,db)[0] == "SELECT first_name, contact_id FROM (contacts)"
    arbre = SyntaxTree("Select(Country,!=,Mali,Difference(cities,Project([Name,Country],cities)))",db)
    arbre.root.display()
    print(SyntaxTree.convertToSQL(arbre.root,db)[0])
    assert SyntaxTree.convertToSQL(SyntaxTree("Select(Country,!=, Mali, Difference(Cities,Project([Name,Country], Cities)))",db).root,db)[0] == ""

    #assert SyntaxTree.convertToSQL(SyntaxTree())
    print("Test three passed")
        


if __name__ == "__main__":
    # regex_test()
    # check_error()
    global_test()
