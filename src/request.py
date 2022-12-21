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

    '''
    Crée la requête SQL et la retourne avec la relation résultante
    '''
    def make_request(self, param, relation : str, table : Relation, db : DataBase):
        # param = (attribut, constante, relation2, operation)
        # param = (string, relation) dans le cas de join, union, difference

        # On vérifie dans chaque cas la validité des attributs par rapport à la relation actuelle (table)     

        if self.type == "Select":

            if table.verifyAttribute(Attribute(param[0],param[2])): # L'attribut existe dans la table et la constante est du bon type
                if(param[1] == "="):
                    obj = Select(Attribute(param[0]), Operation.EQUAL, Constant(param[2]), Relation(relation))
                else:
                    obj = Select(Attribute(param[0]), Operation.DIFFERENT, Constant(param[2]), Relation(relation))
            else:
                if not table.verifyAttribute(Attribute(param[0])): # Vérifie si c'est le nom de colonne ou le type qui est une erreur
                    e = ColumnError(param[0],table.name,db)
                else:
                    e = ColumnError(param[0],table.name,db,param[2])

                raise e

        elif self.type == "Project":
            attributes = [Attribute(attribute) for attribute in param[1:len(param) - 1].split(",")]
            bool = True
            if attributes[0].name == "*": # Cas où on veut tout projetter
                obj = Project(attributes, Relation(relation))
            else:
                for attribute in attributes:
                    if not table.verifyAttribute(attribute):
                        bool = False
                
                if(bool): # Les attributs existent dans la table
                    obj = Project(attributes, Relation(relation))
                    newAttr = []
                    for attribute in table.attributes:
                        if attribute in attributes:
                            newAttr.append(attribute)
                    table.attributes = newAttr
                else:
                    raise ColumnError(attribute.name, table.name, db)

        elif self.type == "Join":
            if not isSubRequest(param[0]): # Gère le cas où la relation est une feuille (table)
                param = (param[0],Relation(param[0]))
                param[1].attributes = db.fetchAllAttributes(param[0])
            
            secondRel = param[0]
            obj = Join(Relation(relation), Relation(secondRel))
            # Fusionne les attributs des deux tables
            for attribute in param[1].attributes:
                if attribute not in table.attributes:
                    table.attributes.append(attribute)


        elif self.type == "Rename":
            ind = param.index(":")
            attribute = Attribute(param[:ind])
            newName = param[(ind+1):]
            if table.verifyAttribute(attribute): # L'attribut existe dans la table
                if not table.verifyAttribute(Attribute(newName)): # Vérifie s'il n'y a pas déjà une colonne avec ce nom
                    obj = Rename(attribute, Constant(newName), Relation(relation))
                    table.attributes[table.attributes.index(attribute)] = Attribute(newName,table.attributes[table.attributes.index(attribute)].ctype) # Renomme l'attribut dans la relation
                else:
                    msg = "An error occured with the rename of "+attribute.name+" to "+newName+" because the table "+table.name+" already contains a column named "+newName
                    error = Exception(msg)
                    raise error
            else:
                raise ColumnError(attribute.name, table.name, db)

        elif self.type == "Union":
            if not isSubRequest(param[0]): # Gère le cas où la relation est une feuille (table)
                param = (param[0],Relation(param[0]))
                param[1].attributes = db.fetchAllAttributes(param[0])

            if table.sameAttributes(param[1].attributes): # Si les attributs sont les mêmes dans les deux relations
                obj = Union(Relation(relation), Relation(param[0]))
            else:
                raise CorrespondingException("Union", table, param[1])

        else:
            if not isSubRequest(param[0]): # Gère le cas où la relation est une feuille (table)
                param = (param[0],Relation(param[0]))
                param[1].attributes = db.fetchAllAttributes(param[0])

            if table.sameAttributes(param[1].attributes): # Si les attributs sont les mêmes dans les deux relations
                obj = Difference(Relation(param[0]), Relation(relation))
            else:
                raise CorrespondingException("Difference", table, param[1])

        self.sql = obj.convert_to_sql() 

        return (self.sql, table)


class CorrespondingException(Exception):
    """
    S'occupe des exceptions dues à la non correspondance des attributs dans le cas d'une union ou d'une difference
    """

    def __init__(self, operation, relation1, relation2) -> None:
        self.operation = operation
        self.relation1 = relation1
        self.relation2 = relation2

    def __str__(self) -> str:
        attrLst1 = self.relation1.attributes
        attrLst2 = self.relation2.attributes
        strg1 = ""
        strg2 = ""
        for i in range(len(attrLst1)):
            strg1 = strg1 +attrLst1[i].name + " "

        for i in range(len(attrLst2)):
            strg2 = strg2 +attrLst2[i].name + " "

        return "An error occured with the operation "+self.operation+". The attributes in the relations does not match.\nThe first relation has the attributes : "+strg1+"and the second relation has the attributes : "+strg2


'''
Vérifie si la requête en paramètre est une sous requête
'''
def isSubRequest(request):
    keywords = ["SELECT","PROJECT","NATURAL JOIN","AS","UNION","FROM"]
    rep = False
    for i in range(len(keywords)):
        if keywords[i] in request:
            rep = True
    return rep
