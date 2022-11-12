"""
Cette classe va s'occuper du bon format du fichier mis en argument.
Cet argument doit correspondre à la forme : nomduficher.db
"""

class FileException(Exception):

    def __init__(self, file : str, details  = "", message = "Error occured with the file") -> None:
        self.file = file
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        s = f"{self.message}\n"
        if(self.details != ""):
            s += f"Details : \"{self.file}\" {self.details}"
        return s