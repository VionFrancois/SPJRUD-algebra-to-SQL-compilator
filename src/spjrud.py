from entities import Expression
from entities import ExpressionWithConstant
from entities import ExpressionWithRelations
from enum import Enum

class Operation(Enum):
    EQUAL = 0
    DIFFERENT = 1

class Select(ExpressionWithConstant):
    """
Please make sure this is the correct syntax : Select(attribute,=/!=,constant,relation)
    """

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
            return f"SELECT * FROM ({self.relation.name}) WHERE ({self.attribute.name}) = '{self.constant.name}'"
        else:
            return f"SELECT * FROM ({self.relation.name}) WHERE ({self.attribute.name}) <> '{self.constant.name}'"


class Project(Expression):
    """
Please make sure this is the correct syntax : Project([attribute1,attribute2, ...],relation) or Project([attribute],relation)
    """

    def __init__(self, attributes, relation):
        self.multiple_projects = [attributes]
        if(type(attributes) == list):
            self.multiple_projects = [Project(attribut, relation) for attribut in attributes]
        else:
            super().__init__("Project",  relation, attributes)

    def __str__(self):
        attributes = ", ".join([attribute.__str__() for attribute in self.multiple_projects])
        return f"Project([{attributes}],{self.relation.__str__()})"

    def convert_to_sql(self):
        attributes = ", ".join([project.attribute.name for project in self.multiple_projects])
        return f"SELECT {attributes} FROM ({self.multiple_projects[0].relation.name})"

class Join(ExpressionWithRelations):
    """
Please make sure this is the correct syntax : Join(relation1,relation2)
    """

    def __init__(self, relation1, relation2):
        super().__init__("Join", relation1, relation2)

    def __str__(self):
        return f"Join({self.relation1.__str__()},{self.relation2.__str__()})"
    
    def convert_to_sql(self):
        return f"SELECT * FROM ({self.relation1.name}) NATURAL JOIN ({self.relation2.name})"

class Rename(ExpressionWithConstant):
    """
Please make sure this is the correct syntax : Rename(attribute,constant,relation)
    """

    def __init__(self, attribute, constant, relation):
        super().__init__("Rename", attribute, relation, constant)

    def __str__(self):
        return f"Rename({self.attribute.__str__()},{self.constant.__str__()},{self.relation.__str__()}"

    def convert_to_sql(self):
        return f"SELECT {self.attribute.name} AS '{self.constant.name}' FROM ({self.relation.name})"

class Union(ExpressionWithRelations):
    """
Please make sure this is the correct syntax : Union(relation1,relation2)
    """

    def __init__(self, relation1, relation2):
        super().__init__("Union", relation1, relation2)

    def __str__(self):
        return f"Union({self.relation1.__str__()},{self.relation2.__str__()}"

    def convert_to_sql(self):
        return f"SELECT * FROM ({self.relation1.name}) UNION SELECT * FROM ({self.relation2.name})"

class Difference(ExpressionWithRelations):
    """
Please make sure this is the correct syntax : Difference(relation1,relation2)
    """

    def __init__(self, relation1, relation2):
            super().__init__("Difference", relation1, relation2)

    def __str__(self):
        return f"Difference({self.relation1.__str__()},{self.relation2.__str__()})"

    def convert_to_sql(self):
        return f"SELECT * FROM ({self.relation1.name}) EXCEPT SELECT * FROM ({self.relation2.name})"
