from entities import Expression, Relation
from enum import Enum

#TODO Dois faire des sous-classes d'Expression pour vérifier les types arg
class Operation(Enum):
    EQUAL = 0
    DIFFERENT = 1

class Select(Expression):

    def __init__(self, attribute, operation, constant, relation):
        if(isinstance(operation, Operation)):
            self.operation = operation
            super().__init__("Select", relation, attribute, constant)


class Project(Expression):
    
    def __init__(self, attribute, relation):
        super().__init__("Project",  relation, attribute)


class Join(Expression):

    def __init__(self, relation1, relation2):
        super().__init__("Join", relation1, None, relation2)

class Rename(Expression):

    def __init__(self, attribute, constant, relation):
        super().__init__("Rename", relation, attribute, constant)

class Union(Expression):

    def __init__(self, relation1, relation2):
        super().__init__("Union", relation1, None, relation2)

class Difference(Expression):

    def __init__(self, relation1, relation2):
        if(isinstance(relation2, Relation)):
            super().init("Difference", relation1, None, relation2)
