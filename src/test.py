from entities import *
from spjrud import *
from SyntaxTree import *

firstReq = "Select(Country,=,Mali,CC)"
secondReq = "Select(id,=,b,Join(b,c))"

arbre = SyntaxTree(firstReq)
print(SyntaxTree.convertToSQL(arbre.root))

arbre.display()