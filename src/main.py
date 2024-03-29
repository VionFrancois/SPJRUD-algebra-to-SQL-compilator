"""
fichier à éxécuter
"""
from sys import argv
from database import *
from request import *
import syntax
from syntaxTree import SyntaxTree

import readline #utilisé pour remplir l'input avec les précédentes requêtes

VERSION = 1

def get_doc():
    res = f"""
######WELCOME TO THE SPJURD COMPILER !######

Creator : François Vion and Julien Ladeuze.
Purpose : database course from the university of Mons.
Version : {VERSION}
Release : 23/12/2022
Goal    : Convert a SPJRUD query into SQL while respecting some constraint such as:
        arity, existence, syntax, ect...

Utils : EXECUTION -> python3 main.py file.db [-h]
                     => 'file.db' must be in the current dir and must be a database file (.db).
                     => '-h' print this documentation.
        PROMPT    -> '&' to get well formatted query from a previous session (from file request.log).
                      When no more query can be requested, returning to the bottom of the file.
                  -> Queries in the SPJRUD format :
                     => SELECT     : Select(attribute, =|!=, constant, relation)
                     => PROJECT    : Project([attribute1,...], relation) 
                        - Put '*' to project all attributes 
                     => JOIN       : Join(relation1, relation2)
                     => RENAME     : Rename(attribute, constant, relation)
                     => UNION      : Union(relation1, relation2)
                     => DIFFERENCE : Difference(relation1, relation2) 
                  -> 'ls table' to list all the tables in the database.
                  -> 'exit' to exit the program
                  -> 'displayTree' after you typed a request.

!PREREQUISITE!
 Python must have the version : 3.10
    """
    return res


def rlinput(prompt, prefill):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()


def get_previous_request(file_name):
    content = []
    with open(file_name, "r") as file:
        content = file.readlines()

    return [x.strip() for x in content]


if __name__ == "__main__":
    LOG = "request.log"

    if "-h" in argv:
        print(get_doc())
        exit()

    if len(argv) < 2:
        print("please put database file as second argument or type python3 main.py -h for more information")
        exit()
    

        
    database = DataBase(argv[1])
    print("please enter a statement.")


    previous_request = get_previous_request(LOG)
    pointer_file = len(previous_request)

    new_request = []
    tree = None
    while True:
        inp = input("-> ")

        while inp == "&" and pointer_file > 0:
            pointer_file -= 1
            inp = rlinput("-> ", previous_request[pointer_file])

        if pointer_file == 0 and inp == "&":
            print("no more request...returning to the bottom")
            pointer_file = len(previous_request)
            continue

        elif inp == "ls table":
            tables = database.fetchAllTables()
            print(f"Number : {len(tables)}\ntables :", end = " ")
            for table in tables:
                print(f"{table}", end = " ")
            print()

        elif inp == "displayTree":
            if tree is not None:
                tree.display()
            else:
                print("Make a valid request before making this command")

        elif inp == "exit":
            break

        else:
            inp = syntax.remove_space(inp)
            if not syntax.syntax_is_correct(inp):
                continue
            else:
                request = None
                # Lancement du programme
                try:
                    tree = SyntaxTree(inp, database)
                    request = SyntaxTree.convertToSQL(tree.root, database)
                    print("\nConverted to SQL : " + request[0])
                    print()
                    database.execute(request[0])
                    database.display()
                except TableNameError as e:
                    print(e)
                except ColumnError as e:
                    print(e)
                except CorrespondingException as e:
                    print(e)
                except Exception as e:
                    print(e)



                if not inp in previous_request:
                    new_request.append(inp)        
    
    with open(LOG, "a") as file:
        for request in new_request:
            file.write(request + "\n")
