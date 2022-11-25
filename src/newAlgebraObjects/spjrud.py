from entities import Expression, ExpressionWithConstant , ExpressionWithRelations
from enum import Enum

class Operation(Enum):
    EQUAL = 0
    DIFFERENT = 1

class Select(ExpressionWithConstant):

    def __init__(self, attribute, operation, constant, relation):
        if(isinstance(operation, Operation)):
            self.operation = operation
            super().__init__("Select", attribute, relation, constant)


class Project(Expression):
    
    def __init__(self, attribute, relation):
        super().__init__("Project",  relation, attribute)


class Join(ExpressionWithRelations):

    def __init__(self, relation1, relation2):
        super().__init__("Join", relation1, relation2)

class Rename(ExpressionWithConstant):

    def __init__(self, attribute, constant, relation):
        super().__init__("Rename", attribute, relation, constant)

class Union(ExpressionWithRelations):

    def __init__(self, relation1, relation2):
        super().__init__("Union", relation1, relation2)

class Difference(ExpressionWithRelations):

    def __init__(self, relation1, relation2):
            super().init("Difference", relation1, relation2)
