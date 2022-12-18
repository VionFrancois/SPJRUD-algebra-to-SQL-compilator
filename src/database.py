import sqlite3
from file import check_file
from entities import Relation, Attribute

class DataBase(object):

    def __init__(self, file_name):
        check_file(file_name)
        self.file_name = file_name
        self.data = None
        self.attributes = None
        
    def execute(self, request):
        try:
            connection = sqlite3.connect(self.file_name)
            cursor = connection.cursor()
            res = cursor.execute(request[0])
            self.data = cursor.fetchall()
            self.attributes = [Attribute(att[0]) for att in cursor.description]
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



class ColumnNameError(Exception):
    """
    S'occupe des exceptions dues à la validation de la requête
    """

    def __init__(self, entity : str, table : str, db : DataBase) -> None:
        self.entity = entity
        self.table = table
        self.db = db
        super().__init__("Error occured with an element")

    def __str__(self) -> str:
        return "An error occured with the element : "+self.entity+". The element does not exist in the table : "+self.table+" or is spelled incorrectly.\n"
        # TODO : Ajouter : "The table "+self.table+" contrains the attibutes : "+self.db.fetchAllAttributes(self.table)


class TableNameError(Exception):

    def __init__(self, table : str, db : DataBase):
        self.table = table
        self.db = db
        super().init("Error occured with a table")

    def __str__(self) -> str:
        return "An error occured with the table : "+self.table+". The table does not exist in the database or is spelled incorrectly.\n"
        # TODO : Ajouter la liste des tables ?