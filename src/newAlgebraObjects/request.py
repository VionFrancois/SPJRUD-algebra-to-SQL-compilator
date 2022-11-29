from spjrud import *
from entities import Attribute, Relation, Constant

class Request(object):

    def __init__(self, Request_type):
        self.type = None
        self.sql = None
        TYPES = ["select","project","join","rename","union","difference"]
        for i in TYPES:
            if(Request_type == i):
                self.type = Request_type 
        if(self.type == None):
            raise Exception() #TODO faire le type de l'exception

    def make_request(self, attribute, relation1, constant = None, relation2 = None, operation = None):
        if self.type == "select":
            if(operation == "="):
                obj = Select(Attribute(attribute, Relation(relation1)), Operation.EQUAL, Constant(constant), Relation(relation1))
            else:
                obj = Select(Attribute(attribute, Relation(relation1)), Operation.DIFFERENT, Constant(constant), Relation(relation1))
        elif self.type == "project":
            obj = Project(Attribute(attribute, Relation(relation1)), Relation(relation1))
        elif self.type == "join":
            obj = Join(Relation(relation1), Relation(relation2))
        elif self.type == "rename":
            obj = Rename(Attribute(attribute, Relation(relation1)), Constant(constant), Relation(relation1))
        elif self.type == "union":
            obj = Union(Relation(relation1), Relation(relation2))
        else:
            obj = Difference(Relation(relation1), Relation(relation2))

        self.sql = obj.convert_to_sql()
        return self.sql
