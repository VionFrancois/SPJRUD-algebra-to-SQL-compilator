from SyntaxTree import *
from AlgebraObjects.Attribute import *
from AlgebraObjects.SPRJUD import *

arbre = SyntaxTree()
attr1 = Attribute("a")
attr2 = Attribute("Select")
attr3 = Attribute("b")
expr = Expression(attr1,attr2,attr3)
arbre.root = Node(expr)

print(arbre.root.left.attribute.name)
print(arbre.root.attribute.name)
print(arbre.root.right.attribute.name)