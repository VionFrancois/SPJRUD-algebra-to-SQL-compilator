from Attribute import Attribute
from Relation import Relation

class Expression(Attribute): #TODO doit encore implementer le fait d'extends d'attribut
    """
    Représente tous les expressions de SPJRUD.
    Inutilisable pour les moments -> voir classe(s) enfant(es)
    """
    def __init__(self, first_attr : Attribute, second_attr : Attribute, relation : Relation) -> None:
        self.first_attr = first_attr
        self.second_attr = second_attr
        self.relation = relation

    def convert_to_sql(self) -> str:
        return None


class Projection(Expression):
    """
    Représente l'opération Projection de SPJRUD.
    """

    def __init__(self, attr : Attribute, relation :  Relation):
        super.__init__(attr, None, relation)

    def __str__(self) -> str:
        return f"Project([{str(self.first_attr)}], {str(self.second_attr)})"

    def convert_to_sql(self):
        return f"select {self.first_attr} from {self.relation}"


class Select(Expression):
    """
    Représente l'opération de selection de SPJRUD
    """

    def __init__(self, first_attr : Attribute, symbol : str, relation : Relation) -> None:
        super.__init__(first_attr, None, relation)
        self.symbol = None
        if symbol == '=' or symbol == '!=':
            self.symbol = symbol
    
    def __str__(self) -> str:
        return f"Select({self.first_attr}, {self.symbol}, {self.second_attr})"

    def convert_to_sql(self):
        return f"SELECT {self.first_attr} FROM {self.relation} WHERE {self.first_attr} = '{self.second_attr}'"

class Rename(Expression):
    """
    Représente l'opération de renommage de SPJRUD
    """

    def __init__(self, first_attr : Attribute, alias : str, relation : Relation) -> None:
        super.__init__(first_attr, None, relation)
        self.alias = alias
        
    def __str__(self) -> str:
        return f"Rename({self.first_attr}, {self.alias}, {self.relation}"
    
    def convert_to_sql(self) -> str:
        return f"SELECT {self.first_attr} AS {self.alias} FROM {self.relation}"

class Join(Expression):
    """
    Représente l'opération de jointure de SPJRUD
    """

    def __init__(self, first_attr : Attribute, second_attr : Attribute, relation : Relation) -> None:
        super.__init__(first_attr, second_attr, relation)

    def __str__(self) -> str:
        return f"Join({self.first_attr}, {self.second_attr}, {self.relation}"

    def convert_to_sql(self) -> str:
        return "" #???

class Union(Expression):
    """
    Représente l'opération d'union de SPJRUD
    """

    def __init__(self, first_attr : Attribute, second_attr : Attribute, relation : Relation) -> None:
        super.__init__(first_attr, second_attr, relation)

    def __str__(self) -> str:
        return f"Union({self.first_attr}, {self.second_attr}, {self.relation}"

    def convert_to_sql(self) -> str:
        return "" #???


class Difference(Expression):
    """
    Représente l'opération de difference de SPJRUD
    """

    def __init__(self, first_attr : Attribute, second_attr : Attribute, relation : Relation) -> None:
        super.__init__(first_attr, second_attr, relation)

    def __str__(self) -> str:
        return f"Difference({self.first_attr}, {self.second_attr}, {self.relation}"

    def convert_to_sql(self) -> str:
        return "" #???