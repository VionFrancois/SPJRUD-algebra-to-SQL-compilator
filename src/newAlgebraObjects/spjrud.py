from newAlgebraObjects.entities import Expression
from newAlgebraObjects.entities import ExpressionWithConstant
from newAlgebraObjects.entities import ExpressionWithRelations
from enum import Enum

class Operation(Enum):
    EQUAL = 0
    DIFFERENT = 1

class Select(ExpressionWithConstant):

    def __init__(self, attribute, operation, constant, relation):
        if(isinstance(operation, Operation)):
            self.operation = operation
            super().__init__("Select", attribute, relation, constant)
    
    def __str__(self):
        if(self.operation == Operation.EQUAL):
            return f"Select({self.attribute.__str__()},=,{self.constant.__str__()},{self.relation})"
        else:
            return f"Select({self.attribute.__str__()},!=,{self.constant.__str__()},{self.relation})"
    
    def convert_to_sql(self):
        if(self.operation == Operation.EQUAL):
            return f"SELECT * FROM {self.relation.name} WHERE {self.attribute.name} = '{self.constant.name}'"
        else:
            return f"SELECT * FROM {self.relation.name} WHERE {self.attribute.name} <> '{self.constant.name}'"


class Project(Expression):
    
    def __init__(self, attribute, relation):
        super().__init__("Project",  relation, attribute)
    
    def __str__(self):
        return f"Project({self.attribute.__str__()},{self.relation.__str__()})"

    def convert_to_sql(self):
        return f"SELECT {self.attribute.name} FROM {self.relation.name}"

class Join(ExpressionWithRelations):

    def __init__(self, relation1, relation2):
        super().__init__("Join", relation1, relation2)

    def __str__(self):
        return f"Join({self.relation1.__str__()},{self.relation2.__str__()})"
    
    def convert_to_sql(self):
        return f"SELECT * FROM {self.relation1.name} NATURAL JOIN {self.relation2.name}"

class Rename(ExpressionWithConstant):

    def __init__(self, attribute, constant, relation):
        super().__init__("Rename", attribute, relation, constant)

    def __str__(self):
        return f"Rename({self.attribute.__str__()},{self.constant.__str__()},{self.relation.__str__()}"

    def convert_to_sql(self):
        return f"SELECT {self.attribute.name} AS '{self.constant.name}' FROM {self.relation.name}"

class Union(ExpressionWithRelations):

    def __init__(self, relation1, relation2):
        super().__init__("Union", relation1, relation2)

    def __str__(self):
        return f"Union({self.relation1.__str__()},{self.relation2.__str__()}"

    def convert_to_sql(self):
        return f"SELECT * FROM {self.relation1.name} UNION SELECT * FROM {self.relation2.name}"

class Difference(ExpressionWithRelations):

    def __init__(self, relation1, relation2):
            super().init("Difference", relation1, relation2)

    def __str__(self):
        return f"Difference({self.relation1.__str__()},{self.relation2.__str__()})"

    def convert_to_sql(self):
        return f"SELECT * FROM {self.relation1.name} EXCEPT SELECT * FROM {self.relation2.name}"
