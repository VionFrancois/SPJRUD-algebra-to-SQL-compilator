"""
fichier à éxécuter
"""
from sys import argv
from file import check_file


if __name__ == "__main__":
    if len(argv) < 2:
        print("please put database as second argument")
        exit()
        
    database = argv[1]
    check_file(database)
    inp = None
    print("please enter a statement.")
    while not(inp == "exit"):
        print("-> ", end = "")
        inp = input()