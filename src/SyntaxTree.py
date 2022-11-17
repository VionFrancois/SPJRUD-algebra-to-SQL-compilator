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
                self.attribute = expression.second_attr
                self.right = Node(expression.thir_attr)
            else:
                if isinstance(attribute, Attribute):   
                    self.attribute = attribute
                    self.left = Node(left)
                    self.right = Node(right)
        else:
            self.attribute = None

    # TODO : Est ce utile en Python ?
    def setLeft(self, attribute):
        self.left = attribute

    def setRight(self, attribute):
        self.right = attribute

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right


    # https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right.attribute is None and self.left.attribute is None:
            line = '%s' % self.attribute.name
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.attribute.name
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.attribute.name
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.attribute.name
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

