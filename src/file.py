"""
Ce module utilisé pour vérifier si le fichier mis en paramètre correspond bien à un 
fichier ".db" et qui se trouve bien dans le répertoire 
"""

from os import listdir, getcwd

def check_file_extension(file : str) -> None:
    if len(file) < 4 or not(file[-3:len(file)] == ".db"):
        raise FileException(file, "doesn't have the right format\nPlease put a file with this format : filename.db")

def check_file_presence(file : str) -> None:
    entries = listdir(getcwd())
    if not(file in entries):
        raise FileException(file, " not found in the current directory")

def check_file(file : str) -> None:
    try:
        check_file_extension(file)  
        check_file_presence(file)
    except FileException as error: 
        print(error)
        exit()


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