from entities import *
from spjrud import *
from SyntaxTree import *

firstReq = "Select(Country,=,Mali,CC)"
secondReq = "Select(id,=,b,Join(b,c))"
thirdReq = "Project([attr1,attr2], Re)"

arbre = SyntaxTree(secondReq)
print(SyntaxTree.convertToSQL(arbre.root))

arbre.display()