from entities import *
from spjrud import *
from SyntaxTree import *

arbre = SyntaxTree()
attr1 = Entity("a")
attr2 = Entity("Select")
attr4 = Entity("b")
attr5 = Entity("c")
attr6 = Expression(attr4, attr2, Entity("d"))
attr3 = Expression(attr4, attr2, attr6)
expr = Expression(attr1,attr2,attr3)
firstReq = "Select(Att(Country),=,Cst(Mali),Re(CC))"
secondReq = "Select(id,=,b,Join(b,c))"

arbre.root = Node(expr)
arbre = SyntaxTree.makeTree(secondReq)

arbre.root.display()

# print(arbre.root.left.attribute.name)
# print(arbre.root.attribute.name)
# print(arbre.root.right.attribute.name)
arbre.display()