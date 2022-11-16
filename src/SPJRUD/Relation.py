
class Relation(object):

    def __init__(self, attributes : list[str], tuples : list[tuple]) -> None:
        self.attributes = attributes
        self.tuples = tuples

    def __str__(self) -> str:
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