from newAlgebraObjects.entities import *
from newAlgebraObjects.spjrud import *

class SyntaxTree():

    def __init__(self) -> None:
        self.root = None


    def makeExpr(self, requete : str):
        # Récupération de l'opérateur
        i = 0
        opStr = ""
        while requete[i] != "(":
            opStr = opStr + requete[i]
        
        param = 2
        match opStr:
            case "Select":
                param = 4
            case "Rename":
                param = 3
        
        # Récupération des opérandes
        paramLst = []
        paramStr = ""
        par = 0
        while param != 0:
            if requete[i] == "(":
                par += 1
            if requete[i] == ")" and par > 0:
                par -= 1
            if (requete[i] == "," or requete[i] == ")") and par == 0:
                paramLst.append(paramStr)
                param -= 1
            else:
                paramStr += param[i]
            
            i += 1
            paramLst.append(paramStr)
            paramStr = ""
        i += 1


        # Crée l'expression avec ses paramètres
        match opStr:
            case "Select":
                expr = Select(param[0], param[1], param[2], param[3])
            case "Project":
                attr = Attribute(param[0])
                rel = Relation(param[1])
                expr = Project(attr, rel)
            case "Join":
                expr = Join(param[0], param[1])
            case "Rename":
                expr = Rename(param[0], param[1], param[2])
            case "Union":
                expr = Union(param[0], param[1])
            case "Difference":
                expr = Difference(param[0], param[1])



        # Cas de base : Feuilles avec une relation qui est une table, pas une expression



        # Cas de réccurence : Expression composée d'une relation qui est une expression
        

        
                        





class Node():

    def __init__(self, entity, left : Entity = None, right : Entity = None) -> None:
        if entity is not None:
            if isinstance(entity, Expression):
                expression = entity
                self.left = Node(expression.first_attr)
                self.entity = expression.second_attr
                self.right = Node(expression.thir_attr)
            else:
                if isinstance(entity, Entity):   
                    self.entity = entity
                    self.left = Node(left)
                    self.right = Node(right)
        else:
            self.entity = None


    # https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right.entity is None and self.left.entity is None:
            line = '%s' % self.entity.name
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.entity.name
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.entity.name
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.entity.name
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

