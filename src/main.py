"""
fichier à éxécuter
"""
from sys import argv
from file import check_file
import sqlite3

if __name__ == "__main__":
    if len(argv) < 2:
        print("please put database as second argument")
        exit()
        
    database = argv[1]
    check_file(database)
    conn = sqlite3.connect(database)
    c = conn.cursor()
   # c.execute("CREATE TABLE contacts (contact_id INTEGER PRIMARY KEY,first_name TEXT NOT NULL,last_name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,phone TEXT NOT NULL UNIQUE);")
    stmt = "insert into contacts (contact_id, first_name, last_name, email, phone) values (?, ?, ?, ?, ?)"
    vals = [(1, 'julien', 'ladeuze', 'julienladeuze@outlook.fr', "0474117240")]
    c.executemany(stmt, vals)
    c.execute("SELECT * FROM contacts")
    print(c.fetchone())
    inp = None
    print("please enter a statement.")
    while not(inp == "exit"):
        print("-> ", end = "")
        inp = input()