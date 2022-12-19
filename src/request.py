from spjrud import *
from entities import Attribute, Relation, Constant
from database import *

class Request(object):
    """
    Va pouvoir effectuer la conversion d'une requête SPJRUD en SQL à partir de chaînes de caractères mises en argument
    """
    def __init__(self, Request_type):
        self.type = None
        self.sql = None
        TYPES = ["Select","Project","Join","Rename","Union","Difference"]
        for i in TYPES:
            if(Request_type == i):
                self.type = Request_type

    def make_request(self, param, relation : str, table : Relation, db : DataBase):
        # param = (attribut, constante, relation2, operation)

        # On vérifie dans chaque cas l'arité des élements par rapport à la relation actuelle (table)     

        if self.type == "Select":

            if table.verifyAttribute(Attribute(param[0])): # L'attribut existe dans la table
                if(param[1] == "="):
                    obj = Select(Attribute(param[0]), Operation.EQUAL, Constant(param[2]), Relation(relation))
                else:
                    obj = Select(Attribute(param[0]), Operation.DIFFERENT, Constant(param[2]), Relation(relation))
            else:
                e = ColumnNameError(param[0],table.name,db)
                raise e

        elif self.type == "Project":
            attributes = [Attribute(attribute) for attribute in param[1:len(param) - 1].split(",")]
            bool = True
            if attributes[0].name == "*": # Cas où on veut tout projetter
                obj = Project(attributes, Relation(relation))
            else:
                for attribute in attributes:
                    if not table.verifyAttribute(attribute):
                        bool = False
                
                if(bool): #Les attributs existent dans la table
                    obj = Project(attributes, Relation(relation))
                    newAttr = []
                    for attribute in table.attributes:
                        if attribute in attributes:
                            newAttr.append(attribute)
                    table.attributes = newAttr
                    # table.attributes = [elem for elem in table.attributes if elem not in attributes]
                else:
                    raise ColumnNameError(attribute.name, table.name, db)

        elif self.type == "Join":
            secondRel = param[0]
            obj = Join(Relation(relation), Relation(secondRel))
            # Fusionne les attributs des deux tables
            for i in range(len(secondRel)):
                if secondRel not in table.attributes:
                    table.attributes.append(secondRel)


        elif self.type == "Rename":
            ind = param.index(":")
            attribute = Attribute(param[:ind])
            if table.verifyAttribute(attribute): # L'attribut existe dans la table
                obj = Rename(attribute, Constant(param[(ind+1):]), Relation(relation))
                table.attributes[table.attributes.index(attribute)] = Attribute(param[(ind+1):]) # Renomme l'attribut dans la relation
            else:
                raise ColumnNameError(attribute.name, table.name, db)

        elif self.type == "Union":
            if table.sameAttributes(param[1].attributes):
                obj = Union(Relation(relation), Relation(param[0]))
            else:
                raise CorrespondingException("Union", table, param[1])
        else:
            if table.sameAttributes(param[1].attributes):
                obj = Difference(Relation(relation), Relation(param[0]))
            else:
                raise CorrespondingException("Difference", table, param[1])

        self.sql = obj.convert_to_sql()

        return (self.sql, table)


class CorrespondingException(Exception):
    """
    S'occupe des exceptions dues à la non correspondance des attributs dans le cas d'une union ou d'une difference
    """

    def __init__(self, operation, relation1, relation2) -> None:
        self.operation = operation
        self.relation1 = relation1
        self.relation2 = relation2

    def __str__(self) -> str:
        attrLst1 = self.relation1.attributes
        attrLst2 = self.relation2.attributes
        strg1 = ""
        strg2 = ""
        for i in range(len(attrLst1)):
            strg1 = strg1 +attrLst1[i].name + " "

        for i in range(len(attrLst2)):
            strg2 = strg2 +attrLst2[i].name + " "

        return "An error occured with the operation "+self.operation+". The attributes in the relations does not match.\nThe first relation has the attributes : "+strg1+"and the second relation has the attributes : "+strg2
