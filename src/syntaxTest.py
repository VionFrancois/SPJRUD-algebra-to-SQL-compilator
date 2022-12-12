import syntax

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
    print("Test one passed.")

#test 2
def check_error():
    assert syntax.syntax_is_correct(syntax.remove_space(f"PROJECT({FIRST_ATTRIBUTE}, {FIRST_RELATION})")) == False
    assert syntax.syntax_is_correct(syntax.remove_space(f"Join({FIRST_RELATION}, {SECOND_RELATION}, re3)")) == False
    assert syntax.syntax_is_correct(syntax.remove_space(f"Project([{FIRST_ATTRIBUTE}, {SECOND_ATTRIBUTE}], {FIRST_RELATION}")) == False
    assert syntax.syntax_is_correct(syntax.remove_space(f"Select({FIRST_ATTRIBUTE}, !==, {CONSTANT}, {FIRST_RELATION})")) == False
    print("Test two passed.")



if __name__ == "__main__":
    regex_test()
    check_error()