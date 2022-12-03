"""
fichier à éxécuter
"""
from sys import argv
from database import DataBase
from request import Request
import syntax



if __name__ == "__main__":
    LOG = "request.log"
    previous_request = []


    if len(argv) < 2:
        print("please put database as second argument")
        exit()
        
    database = DataBase(argv[1])
    inp = None
    print("please enter a statement.")
    with open(LOG, "a") as opened_file:
        while True:
            print("-> ", end = "")
            inp = input()

            if inp == "exit":
                break

            if not syntax.syntax_is_correct(syntax.remove_space(inp)):
                opened_file.write(inp+ "\n")
                continue
            #TODO manque plus que l'execution de la requete apres la décomposition

            
