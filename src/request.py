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
                    obj = Select(Attribute(param[0]), Operation.DIFFERENT, Constant(param[1]), Relation(relation))
            else:
                e = ColumnNameError(param[0],table.name,db)
                raise e

        elif self.type == "Project":
            attributes = [Attribute(attribute) for attribute in param[1:len(param) - 1].split(",")]
            bool = True
            att = None
            if attributes[0] == "*": # Cas où on veut tout projetter
                obj = Project(attributes, Relation(relation))
            else:
                for attribute in attributes:
                    if not table.verifyAttribute(attribute):
                        bool = False
                        att = attribute
                
                if(bool): #Les attributs existent dans la table
                    obj = Project(attributes, Relation(relation))
                    table.attributes = [elem for elem in table.attributes if elem not in attributes]
                else:
                    raise ColumnNameError(attribute.name, table.name, db)

        elif self.type == "Join":
            secondRel = param[0]
            obj = Join(Relation(relation), Relation(secondRel))
            # Fusionne les attributs des deux tables
            for i in range(len(secondRel)):
                if secondRel.attributes[i] not in table.attributes:
                    table.attributes.append(secondRel.attributes[i])


        elif self.type == "Rename":
            if table.verifyAttribute(param[0]): # L'attribut existe dans la table
                obj = Rename(Attribute(param[0]), Constant(param[1]), Relation(relation))
                table.attributes[table.attributes.index(param[0])] = param[0] # Renomme l'attribut dans la relation
            else:
                raise ColumnNameError(param[0].name, table.name, db)

        elif self.type == "Union":
            obj = Union(Relation(relation), Relation(param[0]))
        else:
            obj = Difference(Relation(relation), Relation(param[0]))

        self.sql = obj.convert_to_sql()

        return (self.sql, table)