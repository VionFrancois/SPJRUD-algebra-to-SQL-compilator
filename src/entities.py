"""
Ce fichier représente la base de nos expressions SPJRUD.
Etant donné la complexité de nos classes, une classe InstanceError pourra récuperer 
tous les cas où une exception s'impose
"""

class Entity(object):
    """
    -Représente tout type de d'objet lié aux requêtes SPJRUD comme un attribut, une relation,
     relation, ect...
    -Cette classe sert uniquement pour le référencement polymorphique
    """
    def __init__(self, name, type = None):
        self.name = "unamed"
        self.type = type

        if isinstance(name,str):
            self.name = name
        
        else:
            raise InstanceError(name, str)

class Operator(Entity):
    def __init__(self,name):
        super().__init__(name, 4)


class Attribute(Entity):

    def __init__(self, name):
        super().__init__(name, 2)

    def __eq__(self, obj):
        return isinstance(obj, Attribute) and obj.name == self.name
    
    def __str__(self):
        return self.name



class Relation(Entity):
    """
    Peut représenter deux "type" de relations. 

    Le premier type est celui qui va pouvoir afficher une relation/table.
    En autre, la relation contenant les attributs non nuls "attributes" et "tuples".

    L'autre type servira pour les relations exprimées sous la forme d'une expression SPJURD.
    Cet objet contiendra uniquement un nom (voir la classe Expression pour plus d'info).
    """
    def __init__(self, name, attributes = None, tuples = None):
        super().__init__(name, 1)

        if(type(attributes) == list and all(isinstance(attribute, Attribute) for attribute in attributes) or attributes == None):
            self.attributes = attributes
        elif type(attributes) != list:
            raise InstanceError(attributes, list, True) 
        else:
            raise InstanceError("the content of " + str(attributes) , Attribute)

        if((type(tuples) == list and (len(tuples) == 0 or type(tuples[0]) == tuple)) or tuples == None):
            self.tuples = tuples
        elif(type(tuples) != list):
            raise InstanceError(tuples, list, True)
        else:
            raise InstanceError("the content of " + str(tuples), tuple)

    def verifyAttribute(self, attr : Attribute):
        if attr in self.attributes:
            return True
        else:
            return False

    def sameAttributes(self, lst):
        for attributes in lst:
            if attributes not in self.attributes:
                return False
        return True

        


    """
    affiche une table si et seulement les attributs : attributes et tuples sont non nuls
    Sinon, affiche le nom de la relation    
    """
    def __str__(self) -> str:
        if(self.attributes != None != self.tuples):
            return self.__printTable()
        else:
            return f"relation : {self.name}"

    def __printTable(self):
        length = len(f"{self.attributes[0].name : <25} |") * len(self.attributes)

        s = f"|"
        
        for i in range(0, len(self.attributes)):
            s += f"{self.attributes[i].name.upper() : <25} |"
        
        s += "\n" + "-" * (length + 1) + "\n"

        if(len(self.tuples) != 0):
            for i in range(0, len(self.tuples)):
                s += "|"
                for j in range(0, len(self.tuples[i])):
                    s += f"{self.tuples[i][j] : <25} |"
                s += "\n"
        
        s =f"\n{self.name}:\n\n" + "-" * (length + 1) + "\n" + s + "-" * (length + 1 )+ "\n"
        return s
        


class Constant(Entity):

    def __init__(self, name):
        super().__init__(name, 3)

    def __str__(self):
        return f"constant : {self.name}"


class Expression(Relation):
    """
    Contient tout ce qu'on a besoin pour formuler une expression SPJRUD.
    Cette classe ne peut pas être utilisé pour une instanciation si on veut convertir en SQL (voir module spjurd)
    """
    def __init__(self, name, relation1, attribute = None, relation2 = None, constant = None):
        super().__init__(name)
         
        if(isinstance(attribute, Attribute) or attribute == None):
            self.attribute = attribute
        else:
            raise InstanceError(attribute, Attribute, True)
        
        if(isinstance(relation1, Relation)):
            self.relation1 = relation1
        else:
            raise InstanceError(relation1, Relation) 

        if(isinstance(relation2, Relation) or relation2 == None):
            if(relation2 == None):
                self.relation = self.relation1
            else:
                self.relation2 = relation2
        else:
            raise InstanceError(relation2, Relation, True) 

        if(isinstance(constant, Constant) or constant == None):
            self.constant = constant
        else:
            raise InstanceError(constant, Constant, True) 
    #méthode "abstraite"
    def convert_to_sql(self):
        pass


class ExpressionWithConstant(Expression):
    """
    Sera utilisé pour les expressions : Select et Rename.
    """
    def __init__(self, name, attribute, relation, constant):
        if(isinstance(constant, Constant) and isinstance(attribute, Attribute) and isinstance(relation, Relation)):
            super().__init__(name, relation, attribute, None, constant)
        
        elif(not isinstance(constant, Constant)):
            raise InstanceError(constant, Constant) 

        elif(not isinstance(attribute, Attribute)):
            raise InstanceError(attribute, Attribute)

        else:
            raise InstanceError(relation, Relation)

class ExpressionWithRelations(Expression):
    """
    Sera utilisé pour les expressions : Join, Union, Difference
    """
    def __init__(self, name, relation1, relation2):

        if(isinstance(relation1, Relation) and isinstance(relation2, Relation)):
            super().__init__(name, relation1, None, relation2, None)
        
        elif(not isinstance(relation1, Relation)):
            raise InstanceError(relation1, Relation)

        else:
            raise InstanceError(relation2, Relation) 
        


class InstanceError(Exception):
    """
    Ce type d'exception sera lancé dans le cas où le type d'un argument est invalide
    """
    def __init__(self, arg, class_, can_be_None = False):
        self.message = f"'{arg}' has to be the type of {class_}"
        if(can_be_None):
            self.message = f"{self.message} or can be None"

        super().__init__(self.message)