from SyntaxTree import *
from newAlgebraObjects.entities import *
from newAlgebraObjects.spjrud import *

firstReq = "Select(Att(Country),=,Cst(Mali),Re(CC))"
secondReq = "Select(id,=,b,Join(b,c))"

arbre = SyntaxTree.makeTree(secondReq)

arbre.display()
