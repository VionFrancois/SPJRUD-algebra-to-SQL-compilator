import sqlite3
from file import check_file
from entities import Relation, Attribute

class DataBase(object):

    def __init__(self, file_name):
        check_file(file_name)
        self.file_name = file_name
        self.data = None
        self.attributes = None
        self.name_of_relation = None

    #TODO check existence des attributs
        
    def execute(self, request, name_of_table):
        try:
            connection = sqlite3.connect(self.file_name)
            if(type(name_of_table) != str):
                raise Exception()
            self.name_of_relation = name_of_table
            cursor = connection.execute(request)
            self.data = cursor.fetchall()
            self.attributes = [Attribute(att[0], Relation(self.name_of_relation)) for att in cursor.description]
            self.relation = name_of_table
        except sqlite3.Error as e:
            print(f"The request '{request}' has failed\nDetailed error -> {str(e)}")
        finally:
            connection.close()

    def verify(self, column, table):
        connection = sqlite3.connect(self.file_name)
        cursor = connection.cursor()
        res = cursor.execute("pragma table_info("+table+");")
        data = res.fetchall()
        for i in range(len(data)):
            if data[i][1] == column:
                connection.close()
                return True

        connection.close()
        return False

    def display(self):
        temp = Relation(self.name_of_relation, self.attributes, self.data)
        return temp.__str__()
