from Expression import Expression


class Select(Expression):
    """
    Représente l'opération de selection de SPJRUD
    """

    def __init__(self, first_attr, second_attr, symbol : str,) -> None:
        super.__init__(first_attr, second_attr)
        if symbol == '=' or symbol == '!=':
            super.symbol = symbol
    
    def __str__(self) -> str:
        return f"Select({str(self.first_attr)}, {self.symbol}, {str(self.second_attr)}"