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

            if table.verifyAttribute(param[0]): # L'attribut existe dans la table
                if(param[1] == "="):
                    obj = Select(Attribute(param[0], Relation(relation)), Operation.EQUAL, Constant(param[2]), Relation(relation))
                else:
                    obj = Select(Attribute(param[0], Relation(relation)), Operation.DIFFERENT, Constant(param[1]), Relation(relation))
            else:
                raise ArityException(param[0].name,table.name, db)

        elif self.type == "Project":
            attributes = [Attribute(attribute, Relation(relation)) for attribute in param[1:len(param) - 1].split(",")]
            bool = True
            att = None
            for attribute in attributes:
                if not table.verifyAttribute(attribute):
                    bool = False
                    att = attribute
            
            if(bool): #Les attributs existent dans la table
                obj = Project(attributes, Relation(relation))
            else:
                raise ArityException(attribute.name, table.name, db)

        elif self.type == "Join":
            obj = Join(Relation(relation), Relation(param[0]))
        elif self.type == "Rename":

            if table.verifyAttribute(param[0]): # L'attribut existe dans la table
                obj = Rename(Attribute(param[0], Relation(relation)), Constant(param[1]), Relation(relation))
            else:
                raise ArityException(param[0].name, table.name, db)

        elif self.type == "Union":
            obj = Union(Relation(relation), Relation(param[0]))
        else:
            obj = Difference(Relation(relation), Relation(param[0]))

        self.sql = obj.convert_to_sql()
        # TODO : Retourner la table résultante de l'opération
        return (self.sql, table)