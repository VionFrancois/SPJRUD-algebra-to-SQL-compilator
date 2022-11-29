import sqlite3
from file import check_file
from entities import Relation, Attribute

class DataBase(object):

    def __init__(self, file_name):
        check_file(file_name)
        self.file_name = file_name
        self.connection = sqlite3.connect(file_name)
        self.data = None
        self.attributes = None
        self.name_of_relation = None
        stmt = "insert into contacts (contact_id, first_name, last_name, email, phone) values (?, ?, ?, ?, ?)"
        vals = [(1, 'julien', 'ladeuze', 'julienladeuze@outlook.fr', "0474117240")]
        self.connection.executemany(stmt, vals)
        stmt = "insert into contacts (contact_id, first_name, last_name, email, phone) values (?, ?, ?, ?, ?)"
        vals = [(2, 'jqgegqeeq', 'lgqq', 'mfqghfqgqqg', "6079900790")]
        self.connection.executemany(stmt, vals)
        
    def execute(self, request, name_of_relation):
        if(type(name_of_relation) != str):
            raise Exception()
        self.name_of_relation = name_of_relation
        cursor = self.connection.execute(request)
        self.data = cursor.fetchall()
        self.attributes = [Attribute(att[0], Relation(self.name_of_relation)) for att in cursor.description]
        self.relation = name_of_relation

    def display(self):
        temp = Relation(self.name_of_relation, self.attributes, self.data)
        return temp.__str__()
