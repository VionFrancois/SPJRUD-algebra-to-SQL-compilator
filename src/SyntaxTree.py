from newAlgebraObjects.entities import *
from newAlgebraObjects.spjrud import *

class SyntaxTree():

    def __init__(self) -> None:
        self.root = None

    def isSubRequest(request):
        keywords = ["Select(","Project(","Join(","Rename(","Union(","Difference("]
        rep = False
        for i in range(len(keywords)):
            if keywords[i] in request:
                rep = True
        return rep

    def makeTree(requete : str):
        # Récupération de l'opérateur
        i = 0
        opStr = ""
        while requete[i] != "(":
            opStr = opStr + requete[i]
            i += 1
        
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
        i += 1
        while param != 0:
            if requete[i] == "(":
                par += 1
            if requete[i] == ")" and par > 0:
                par -= 1
            if (requete[i] == ",") and par == 0:
                paramLst.append(paramStr)
                paramStr = ""
                param -= 1
            else:
                paramStr += requete[i]

            if(i == len(requete) -1):
                paramLst.append((paramStr[:-1]))
                param -= 1
            i += 1


        # Crée le sous arbre avec les paramètres
        # Pour chaque cas, on a :
        # Cas de base : Feuilles avec une relation qui est une table, pas une expression
        # Cas de réccurence : Expression composée d'une relation qui est une expression

        match opStr:
            case "Select":

                subTree = Node(Entity("Select"))
                subTree.left = Node(Entity(paramLst[1])) # Opérateur
                subTree.left.left = Node(Entity(paramLst[0])) # Attribut
                subTree.left.right = Node((Entity(paramLst[2]))) # Constante

                if SyntaxTree.isSubRequest(paramLst[3]):
                    subTree.right = SyntaxTree.makeTree(paramLst[3]) # Crée le sous arbre de la requête
                else:
                    subTree.right = Node(Entity(paramLst[3])) # Relation (table)
                  
            case "Project":

                subTree = Node(Entity("Project"))
                subTree.left = Node(Entity(paramLst[0])) # Attribut

                if SyntaxTree.isSubRequest(paramLst[1]):
                    subTree.right = SyntaxTree.makeTree(paramLst[1]) # Crée le sous arbre de la requête
                else:
                    subTree.right = Node(Entity(paramLst[1])) # Relation (table)
                
            case "Join":

                subTree = Node(Entity("Join"))

                if SyntaxTree.isSubRequest(paramLst[0]):
                    subTree.left = SyntaxTree.makeTree(paramLst[0]) # Crée le sous arbre de la requête
                else:
                    subTree.left = Node(Entity(paramLst[1])) # Relation (table)

                if SyntaxTree.isSubRequest(paramLst[1]):
                    subTree.right = SyntaxTree.makeTree(paramLst[1]) # Crée le sous arbre de la requête
                else:
                    subTree.right = Node(Entity(paramLst[1])) # Relation (table)

            case "Rename":

                subTree = Node(Entity("Rename"))
                subTree.left = Node(Entity(paramLst[0]+":"+paramLst[1])) # ancienNom:nouveauNom

                if SyntaxTree.isSubRequest(paramLst[2]):
                    subTree.right = SyntaxTree.makeTree(paramLst[2]) # Crée le sous arbre de la requête
                else:
                    subTree.right = Node(Entity(paramLst[2])) # Relation (table)

            case "Union":

                subTree = Node(Entity("Union"))

                if SyntaxTree.isSubRequest(paramLst[0]):
                    subTree.left = SyntaxTree.makeTree(paramLst[0]) # Crée le sous arbre de la requête
                else:
                    subTree.left = Node(Entity(paramLst[1])) # Relation (table)

                if SyntaxTree.isSubRequest(paramLst[1]):
                    subTree.right = SyntaxTree.makeTree(paramLst[1]) # Crée le sous arbre de la requête
                else:
                    subTree.right = Node(Entity(paramLst[1])) # Relation (table)

            case "Difference":

                subTree = Node(Entity("Difference"))

                if SyntaxTree.isSubRequest(paramLst[0]):
                    subTree.left = SyntaxTree.makeTree(paramLst[0]) # Crée le sous arbre de la requête
                else:
                    subTree.left = Node(Entity(paramLst[1])) # Relation (table)

                if SyntaxTree.isSubRequest(paramLst[1]):
                    subTree.right = SyntaxTree.makeTree(paramLst[1]) # Crée le sous arbre de la requête
                else:
                    subTree.right = Node(Entity(paramLst[1])) # Relation (table)

        return subTree


        

        
                        





class Node():

    def __init__(self, entity) -> None:
        if entity is not None:
            # if isinstance(entity, Expression):
            #     expression = entity
            #     self.left = Node(expression.first_attr)
            #     self.entity = expression.second_attr
            #     self.right = Node(expression.thir_attr)
            # else:
                if isinstance(entity, Entity):   
                    self.entity = entity
                    self.left = Node(None)
                    self.right = Node(None)
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

