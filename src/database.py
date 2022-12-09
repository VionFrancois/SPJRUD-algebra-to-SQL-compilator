import sqlite3
from file import check_file
from entities import Relation, Attribute

class DataBase(object):

    def __init__(self, file_name):
        check_file(file_name)
        self.file_name = file_name
        self.data = None
        self.attributes = None

    #TODO check existence des attributs
        
    def execute(self, request):
        try:
            connection = sqlite3.connect(self.file_name)
            cursor = connection.cursor().execute(request)
            self.data = cursor.fetchall()
            self.attributes = [Attribute(att[0], "resulting table") for att in cursor.description]
            connection.close()
        except sqlite3.Error as e:
            print(f"The request '{request}' has failed\nDetailed error -> {str(e)}")

    def verifyAtt(self, column, table):
        connection = sqlite3.connect(self.file_name)
        cursor = connection.cursor()
        res = cursor.execute("pragma table_info("+table+")")
        data = res.fetchall()
        for i in range(len(data)):
            if data[i][1] == column:
                connection.close()
                return True

        connection.close()
        return False

    def verifyTable(self, table):
        connection = sqlite3.connect(self.file_name)
        cursor = connection.cursor()
        res = cursor.execute("pragma table_info("+table+")")
        data = res.fetchall()
        if data == []:
            connection.close()
            return False

        connection.close()
        return True

    def display(self):
        temp = Relation("resulting table", self.attributes, self.data)
        return temp.__str__()
