from spjrud import *
from entities import Attribute, Relation, Constant

class Request(object):

    def __init__(self, Request_type):
        self.type = None
        self.sql = None
        TYPES = ["Select","Project","Join","Rename","Union","Difference"]
        for i in TYPES:
            if(Request_type == i):
                self.type = Request_type 
        if(self.type == None):
            raise Exception() #TODO faire le type de l'exception

    def make_request(self, param, relation):
        # param = (attribut, constante, relation2, operation)
        if self.type == "Select":
            if(param[1] == "="):
                obj = Select(Attribute(param[0], Relation(relation)), Operation.EQUAL, Constant(param[2]), Relation(relation))
            else:
                obj = Select(Attribute(param[0], Relation(relation)), Operation.DIFFERENT, Constant(param[1]), Relation(relation))
        elif self.type == "Project":
            # TODO : Convertir le multi paramètres (string) en liste
            obj = Project(Attribute(param[0], Relation(relation)), Relation(relation))
        elif self.type == "Join":
            obj = Join(Relation(relation), Relation(param[0]))
        elif self.type == "Rename":
            obj = Rename(Attribute(param[0], Relation(relation)), Constant(param[1]), Relation(relation))
        elif self.type == "Union":
            obj = Union(Relation(relation), Relation(param[0]))
        else:
            obj = Difference(Relation(relation), Relation(param[0]))

        self.sql = obj.convert_to_sql()
        return self.sql
