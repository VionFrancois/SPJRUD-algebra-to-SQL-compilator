from SyntaxTree import *
from newAlgebraObjects.entities import *
from newAlgebraObjects.spjrud import *

arbre = SyntaxTree()
attr1 = Entity("a")
attr2 = Entity("Select")
attr4 = Entity("b")
attr5 = Entity("c")
attr6 = Expression(attr4, attr2, Entity("d"))
attr3 = Expression(attr4, attr2, attr6)
expr = Expression(attr1,attr2,attr3)

arbre.root = Node(expr)

arbre.root.display()

# print(arbre.root.left.attribute.name)
# print(arbre.root.attribute.name)
# print(arbre.root.right.attribute.name)