"""
fichier à executer
"""
from sys import argv
from file import check_file


if __name__ == "__main__":
    database = argv[1]
    check_file(database)
    inp = None
    print("please enter a statement.")
    while not(inp == "exit"):
        print("-> ", end = "")
        inp = input()