class Entity(object):

    def __init__(self, name):
        self.name = "unamed"

        if(type(name) == str):
            self.name = name
        
    def __str__(self):
        return f"Entity : {self.name}"

class Relation(Entity):

    def __init__(self, name, attributes = None, tuples = None):
        super().__init__(name)

        if(isinstance(attributes, list[Attribute]) or attributes == None):
            self.attributes = attributes
        else:
            raise Exception() #TODO doit penser à l'exception

        if(isinstance(tuples,list[tuple]) or tuples == None):
            self.tuples = tuples
        else:
            raise Exception() #TODO doit penser à l'exception

    def __str__(self) -> str:
        if(self.attributes != None != self.tuples):
            return self.printTable()

    def __printTable(self):
        length = len(f"{self.attributes[0] : <15} |") * len(self.attributes)

        s = "|"
        
        for i in range(0, len(self.attributes)):
            s += f"{self.attributes[i].upper() : <15} |"
        
        s += "\n" + "-" * (length + 1) + "\n"

        for i in range(0, len(self.tuples)):
            s += "|"
            for j in range(0, len(self.tuples[i])):
                s += f"{self.tuples[i][j] : <15} |"
            s += "\n"
        
        s = "-" * (length + 1) + "\n" + s + "-" * (length + 1 )+ "\n"
        return s
        


class Attribute(Entity):
    
    def __init__(self, name, relation):
        super().__init__(name)

        if(isinstance(relation ,Relation)):
            self.relation = relation
        else:
            raise Exception() #TODO doit penser à l'exception
    
    def __str__(self):
        return super.__str__()


class Constant(Entity):

    def __init__(self, name):
        super().__init__(name)

        if(type(name) == str):
            self.CONSTANT = name #_attribut -> protected
        else:
            raise Exception() #TODO doit penser à l'exception


class Expression(Relation):

    def __init__(self, name, relation1, attribute = None, relation2 = None, constant = None):
        super().__init__(name)

        if(isinstance(attribute, Attribute)):
            self.attribute = attribute
        else:
            raise Exception() #TODO doit penser à l'exception
        
        if(isinstance(relation1, Relation)):
            self.relation1 = relation1
        else:
            raise Exception() #TODO doit penser à l'exception

        if(isinstance(relation2, Relation) or relation2 == None):
            if(relation2 == None):
                self.relation = self.relation1
            else:
                self.relation2 = relation2
        else:
            raise Exception() #TODO doit penser à l'exception
        if(isinstance(constant, Constant) or constant == None):
            self.constant = constant
        else:
            raise Exception() #TODO doit penser à l'exception
        
