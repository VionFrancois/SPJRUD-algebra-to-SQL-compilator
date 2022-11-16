from AlgebraObjects.Attribute import Attribute
from AlgebraObjects.SPRJUD import Expression

class SyntaxTree():

    def __init__(self) -> None:
        self.root = None

    def setRoot(self, attribute):
        self.root = attribute

    def getRoot(self):
        return self.root


class Node():

    def __init__(self, attribute, left : Attribute = None, right : Attribute = None) -> None:
        if attribute is not None:
            if isinstance(attribute, Expression):
                expression = attribute
                self.left = Node(expression.first_attr)
                self.attribute = Node(expression.second_attr)
                self.right = Node(expression.thir_attr)
            else:
                if isinstance(attribute, Attribute):   
                    self.attribute = attribute
                    self.left = Node(left)
                    self.right = Node(right)

    def setLeft(self, attribute):
        self.left = attribute

    def setRight(self, attribute):
        self.right = attribute

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    # def addExpression(self, expression : Expression):
    #     self.left = expression.first_attr
    #     self.root = expression.second_attr
    #     self.right = expression.third_attr

