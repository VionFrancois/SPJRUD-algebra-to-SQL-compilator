from SyntaxTree import *
from AlgebraObjects.Attribute import *
from AlgebraObjects.SPRJUD import *

arbre = SyntaxTree()
attr1 = Attribute("a")
attr2 = Attribute("Select")
attr4 = Attribute("b")
attr5 = Attribute("c")
attr3 = Expression(attr4, attr2, attr5)
expr = Expression(attr1,attr2,attr3)
arbre.root = Node(expr)

arbre.root.display()

# print(arbre.root.left.attribute.name)
# print(arbre.root.attribute.name)
# print(arbre.root.right.attribute.name)