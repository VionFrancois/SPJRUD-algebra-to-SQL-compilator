from FileException import FileException
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
        # TODO : check_file_presence(file)
    except FileException as error: 
        print(error)
        exit()
