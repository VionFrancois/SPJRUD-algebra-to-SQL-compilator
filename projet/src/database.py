import sqlite3
from file import check_file
from entities import Relation, Attribute

class DataBase(object):

    def __init__(self, file_name):
        check_file(file_name)
        self.file_name = file_name
        self.data = None
        self.attributes = None
        
    '''
    Execute une requête SQL sur la base de donnée
    '''
    def execute(self, request):
        try:
            connection = sqlite3.connect(self.file_name)
            cursor = connection.cursor()
            res = cursor.execute(request)
            self.data = cursor.fetchall()
            self.attributes = [Attribute(att[0]) for att in cursor.description]
        except sqlite3.Error as e:
            print(f"The request '{request}' has failed\nDetailed error -> {str(e)}")
            raise Exception("")
        finally:
            cursor.close()
            connection.close()


    '''
    Retourne tout les attributs d'une table
    '''
    def fetchAllAttributes(self, table):
        connection = sqlite3.connect(self.file_name)
        cursor = connection.cursor()
        res = cursor.execute("pragma table_info("+table+")")
        data = res.fetchall()
        attributes = []
        for i in range(len(data)):
            attributes.append(Attribute(data[i][1], data[i][2]))  

        connection.close()
        return attributes


    '''
    Vérifie l'existance d'une table dans la base de données
    '''
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

    '''
    Retourne toutes les table de la base de données
    '''
    def fetchAllTables(self):
        connection = sqlite3.connect(self.file_name)
        cursor = connection.cursor()
        res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        data = res.fetchall()
        tables = []
        for i in range(len(data)):
            tables.append(data[i][0])  

        connection.close()
        return tables
         

    def display(self):
        # TODO : Print toujours resulting table
        temp = Relation("resulting table", self.attributes, self.data)
        print(temp.__str__())



class ColumnError(Exception):
    """
    Gère les erreurs dûes à un attribut
    """

    def __init__(self, entity : str, table : str, db : DataBase, ctype = None) -> None:
        self.entity = entity
        self.table = table
        self.db = db
        self.ctype = ctype
        
        if ctype is None: # Erreur dûe au nom de l'attribut
            attrLst = self.db.fetchAllAttributes(self.table)
            strg = ""
            for i in range(len(attrLst)):
                strg = strg +attrLst[i].name + " "

            self.msg = "An error occured with the element : "+self.entity+". The element does not exist in the table : "+self.table+" or is spelled incorrectly.\nThe table "+self.table+" contrains the attibutes : "+strg
        else: # Erreur dûe au type d'une constante
            attrLst = self.db.fetchAllAttributes(self.table)
            type = attrLst[attrLst.index(Attribute(self.entity))].ctype
            self.msg = "An error occured with the element : "+self.ctype+". The element does not match the expecting type of "+self.entity+" which is "+type

        super().__init__("Error occured with an element")

    def __str__(self) -> str:
        return self.msg


class TableNameError(Exception):
    '''
    Gère les erreurs dûes au mauvais nom d'une table
    '''
    def __init__(self, table : str, db : DataBase):
        self.table = table
        self.db = db

    def __str__(self) -> str:
        tbLst = self.db.fetchAllTables()
        strg = ""
        for i in range(len(tbLst)):
            strg = strg +tbLst[i] + " "
        return "An error occured with the table : "+self.table+". The table does not exist in the database or is spelled incorrectly.\nThe database contains the tables : "+strg