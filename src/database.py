import sqlite3
from file import check_file
from entities import Relation, Attribute

class DataBase(object):

    def __init__(self, file_name):
        check_file(file_name)
        self.file_name = file_name
        self.data = None
        self.attributes = None
        
    # TODO : Gérer le cas de rename dans le bas de l'arbre

    def execute(self, request):
        try:
            connection = sqlite3.connect(self.file_name)
            cursor = connection.cursor()
            res = cursor.execute(request)
            self.data = cursor.fetchall()
            self.attributes = [Attribute(att[0], Relation("resulting table")) for att in cursor.description]
        except sqlite3.Error as e:
            print(f"The request '{request}' has failed\nDetailed error -> {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def fetchAllAttributes(self, table):
        connection = sqlite3.connect(self.file_name)
        cursor = connection.cursor()
        res = cursor.execute("pragma table_info("+table+")")
        data = res.fetchall()
        attributes = []
        for i in range(len(data)):
            attributes.append(Attribute(data[i][1]))  

        connection.close()
        return attributes


    # TODO : Obsolète
    def verifyAtt(self, column, table):
        attributes = self.fetchAllAttributes(table)
        if column in attributes:
            return True
        else:
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
        print(temp.__str__())



class ArityException(Exception):
    """
    S'occupe des exceptions dues à la validation de la requête
    """

    def __init__(self, entity : str, table : str, db : DataBase) -> None:
        self.entity = entity
        self.table = table
        self.db = db
        super().__init__("Error occured with the arity of an element")

    def __str__(self) -> str:
        return "An error occured with the element : "+self.entity+". The element does not exist in the table : "+self.table+" or is spelled incorrectly.\n" + "The table "+self.table+" contrains the attibutes : "+self.db.fetchAllAttributes