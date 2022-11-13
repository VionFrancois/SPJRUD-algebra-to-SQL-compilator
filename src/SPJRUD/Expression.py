from Attribute import Attribute
from Relation import Relation

class Expression(object):
    """
    Représente tous les expressions de SPJRUD.
    Inutilisable pour les moments -> voir classe(s) enfant(es)
    """
    def __init__(self, first_attr : Attribute, second_attr : Attribute, relation : str) -> None: #relation 
        self.first_attr = first_attr
        self.second_attr = second_attr
