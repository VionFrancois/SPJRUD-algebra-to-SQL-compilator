"""
fichier à éxécuter
"""
from sys import argv
from database import DataBase
from request import Request
import syntax
from SyntaxTree import SyntaxTree

import readline #utilisé pour remplir l'input avec les précédentes requêtes


#https://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible/2533142#2533142
def rlinput(prompt, prefill='test'):
   print(prompt, end = "")
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input()  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()


def get_previous_request(file_name):
    content = []
    with open(file_name, "r") as file:
        content = file.readlines()

    return [x.strip() for x in content]


if __name__ == "__main__":
    LOG = "request.log"


    # if len(argv) < 2:
    #     print("please put database as second argument")
    #     exit()
        
    #database = DataBase(argv[1])
    database = DataBase("src/test.db")
    print("please enter a statement.")
    print(database.verifyAtt("contacts","osef"))
    print(database.verifyTable("UwU"))


    previous_request = get_previous_request(LOG)
    pointer_file = len(previous_request)

    new_request = []

    while True:
        print("-> ", end = "")
        inp = input()

        while inp == "&" and pointer_file > 0:
            pointer_file -= 1
            inp = rlinput("-> ", previous_request[pointer_file])
        
        if inp == "exit":
            break

        if pointer_file == 0 and inp == "&":
            print("no more request...returning to the bottom")
            pointer_file = len(previous_request)
            continue

        inp = syntax.remove_space(inp)
        if not syntax.syntax_is_correct(inp):
            continue
        else:
            tree = SyntaxTree(inp)
            request = SyntaxTree.convertToSQL(tree.root)
            print("\nConverted to SQL : " + request)
            database.execute(request)
            database.display()
            if not inp in previous_request:
                new_request.append(inp)        
    
    with open(LOG, "a") as file:
        for request in new_request:
            file.write(request + "\n")


"""
Constaté un bug, on peut delete le prompt
"""