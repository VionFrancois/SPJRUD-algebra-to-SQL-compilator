class FileException(Exception):
    """
    S'occupe de toutes les exceptions générées dues au fichier mis
    en paramètre lors de l'éxécution du programme.
    """

    def __init__(self, file : str, details  = "", message = "Error occured with the file") -> None:
        self.file = file
        self.message = message
        self.details = details
        super().__init__("Error occured with the file")

    def __str__(self) -> str:
        s = f"{self.message}\n"
        if(self.details != ""):
            s += f"Details : \"{self.file}\" {self.details}"
        return s

# TODO : Fusionner avec file.py ?