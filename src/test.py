from entities import *
from spjrud import *
from SyntaxTree import *

firstReq = "Select(Att(Country),=,Cst(Mali),Re(CC))"
secondReq = "Select(id,=,b,Join(b,c))"

arbre = SyntaxTree.makeTree(secondReq)

arbre.display()