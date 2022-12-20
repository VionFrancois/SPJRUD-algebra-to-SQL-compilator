from entities import *
from spjrud import *
from request import *
from database import *

class Node():

    def __init__(self, entity) -> None:
        if entity is not None:
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


class SyntaxTree():

    def __init__(self, request : str,db : DataBase) -> None:
        self.root = SyntaxTree.makeTree(request,db)

    
    '''
    Vérifie si la requête en paramètre est une sous requête
    '''
    def isSubRequest(request):
        keywords = ["Select(","Project(","Join(","Rename(","Union(","Difference("]
        rep = False
        for i in range(len(keywords)):
            if keywords[i] in request:
                rep = True
        return rep

    '''
    Crée l'arbre de syntaxe recursivement à partir d'un string (suivant la bonne syntaxe)
    '''
    def makeTree(requete : str, db : DataBase):
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
        crochet = False # Permet de gérer le cas de plusieurs paramètres dans Project
        par = 0
        i += 1
        while param != 0:
            if requete[i] == "(":
                par += 1
            if requete[i] == ")" and par > 0:
                par -= 1
            if (requete[i] == ",") and par == 0 and not crochet:
                paramLst.append(paramStr)
                paramStr = ""
                param -= 1
            else:
                if requete[i] == "[":
                    crochet = True
                elif requete[i] == "]":
                    crochet = False

                paramStr += requete[i]

            if(i == len(requete) -1):
                paramLst.append((paramStr[:-1]))
                param -= 1
            i += 1


        # Crée le sous arbre avec les paramètres
        # Pour chaque cas, on a :
        # Cas de base : Feuilles avec une relation qui est une table ou un attribut, pas une expression
        # Cas de récurrence : Expression composée d'une relation qui est une expression

        match opStr:
            case "Select":

                subTree = Node(Entity("Select"))
                subTree.left = Node(Operator(paramLst[1])) # Opérateur
                subTree.left.left = Node(Attribute(paramLst[0])) # Attribut
                subTree.left.right = Node(Constant(paramLst[2])) # Constante

                if SyntaxTree.isSubRequest(paramLst[3]):
                    subTree.right = SyntaxTree.makeTree(paramLst[3], db) # Crée le sous arbre de la requête
                else:
                    if db.verifyTable(paramLst[3]): # Vérification de l'existance de la table
                        subTree.right = Node(Relation(paramLst[3], db.fetchAllAttributes(paramLst[3]))) # Relation (table)
                    else:
                        raise TableNameError(paramLst[3], db)
                  
            case "Project":

                subTree = Node(Entity("Project"))
                subTree.left = Node(Attribute(paramLst[0])) # Attribut

                if SyntaxTree.isSubRequest(paramLst[1]):
                    subTree.right = SyntaxTree.makeTree(paramLst[1], db) # Crée le sous arbre de la requête
                else:
                    if db.verifyTable(paramLst[1]): # Vérification de l'existance de la table
                        subTree.right = Node(Relation(paramLst[1], db.fetchAllAttributes(paramLst[1]))) # Relation (table)
                    else:
                        raise TableNameError(paramLst[1], db)
                
            case "Join":

                subTree = Node(Entity("Join"))

                if SyntaxTree.isSubRequest(paramLst[0]):
                    subTree.left = SyntaxTree.makeTree(paramLst[0], db) # Crée le sous arbre de la requête
                else:
                    if db.verifyTable(paramLst[0]): # Vérification de l'existance de la table
                        subTree.left = Node(Relation(paramLst[0], db.fetchAllAttributes(paramLst[0]))) # Relation (table)
                    else:
                        raise TableNameError(paramLst[0], db)

                if SyntaxTree.isSubRequest(paramLst[1]): 
                    subTree.right = SyntaxTree.makeTree(paramLst[1], db) # Crée le sous arbre de la requête
                else:
                    if db.verifyTable(paramLst[1]): # Vérification de l'existance de la table
                        subTree.right = Node(Relation(paramLst[1], db.fetchAllAttributes(paramLst[1]))) # Relation (table)
                    else:
                        raise TableNameError(paramLst[1], db)

            case "Rename":

                subTree = Node(Entity("Rename"))
                subTree.left = Node(Entity(paramLst[0]+":"+paramLst[1])) # ancienNom:nouveauNom

                if SyntaxTree.isSubRequest(paramLst[2]):
                    subTree.right = SyntaxTree.makeTree(paramLst[2], db) # Crée le sous arbre de la requête
                else:
                    if db.verifyTable(paramLst[2]): # Vérification de l'existance de la table
                        subTree.right = Node(Relation(paramLst[2], db.fetchAllAttributes(paramLst[2]))) # Relation (table)
                    else:
                        raise TableNameError(paramLst[2], db)

            case "Union":

                subTree = Node(Entity("Union"))

                if SyntaxTree.isSubRequest(paramLst[0]):
                    subTree.left = SyntaxTree.makeTree(paramLst[0], db) # Crée le sous arbre de la requête
                else:
                    if db.verifyTable(paramLst[0]): # Vérification de l'existance de la table
                        subTree.left = Node(Relation(paramLst[0], db.fetchAllAttributes(paramLst[0]))) # Relation (table)
                    else:
                        raise TableNameError(paramLst[0], db)
                        
                if SyntaxTree.isSubRequest(paramLst[1]):
                    subTree.right = SyntaxTree.makeTree(paramLst[1], db) # Crée le sous arbre de la requête
                else:
                    if db.verifyTable(paramLst[1]): # Vérification de l'existance de la table
                        subTree.right = Node(Relation(paramLst[1], db.fetchAllAttributes(paramLst[1]))) # Relation (table)
                    else:
                        raise TableNameError(paramLst[1], db)

            case "Difference":

                subTree = Node(Entity("Difference"))

                if SyntaxTree.isSubRequest(paramLst[0]):
                    subTree.left = SyntaxTree.makeTree(paramLst[0], db) # Crée le sous arbre de la requête
                else:
                    if db.verifyTable(paramLst[0]): # Vérification de l'existance de la table
                        subTree.left = Node(Relation(paramLst[0], db.fetchAllAttributes(paramLst[0]))) # Relation (table)
                    else:
                        raise TableNameError(paramLst[0], db)

                if SyntaxTree.isSubRequest(paramLst[1]):
                    subTree.right = SyntaxTree.makeTree(paramLst[1], db) # Crée le sous arbre de la requête
                else:
                    if db.verifyTable(paramLst[1]): # Vérification de l'existance de la table
                        subTree.right = Node(Relation(paramLst[1], db.fetchAllAttributes(paramLst[1]))) # Relation (table)
                    else:
                        raise TableNameError(paramLst[1], db)
        return subTree


    '''
    Convertit recursivement un SyntaxTree en une requête SQL (string) en effectuant un parcours postordre
    '''
    def convertToSQL(arbre : Node, db : DataBase):
        # Cas de base : L'arbre est une feuille et retourne son élément
        # Cas de récurrence : L'arbre n'est pas une feuille et est donc une expression ou un opérateur

        # Si c'est une feuille
        if arbre.left.entity is None and arbre.right.entity is None:
            if arbre.entity.type == 1: # Relation (table)
                return (arbre.entity.name, arbre.entity)
            else:
                return arbre.entity.name
        
        else: # Si c'est un noeud interne
            left = SyntaxTree.convertToSQL(arbre.left, db) # Convertit le sous-arbre gauche
            right = SyntaxTree.convertToSQL(arbre.right, db) # Convertit le sous-arbre droitr
            
            # Traite le noeud actuel
            racine = arbre.entity

            # Cas où le noeud interne est l'opération = ou != de Select
            if racine.name == "=" or racine.name == "!=":
                return (left, racine.name, right)
            else:
                request = Request(arbre.entity.name)
                return request.make_request(left,right[0],right[1],db) # Retourne la requête avec la relation résultante

    ''''
    Permet d'afficher l'arbre syntaxique dans le terminal
    '''
    def display(self):
        self.root.display()