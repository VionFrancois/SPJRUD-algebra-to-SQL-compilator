from request import Request
import sqlite3

request = Request("select")
s = request.make_request("attrib", "relat", "const", None, "=")
print(s)
database = "test.db"
conn = sqlite3.connect(database)
c = conn.cursor()
#c.execute("CREATE TABLE contacts (contact_id INTEGER PRIMARY KEY,first_name TEXT NOT NULL,last_name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,phone TEXT NOT NULL UNIQUE);")
stmt = "insert into contacts (contact_id, first_name, last_name, email, phone) values (?, ?, ?, ?, ?)"
vals = [(1, 'julien', 'ladeuze', 'julienladeuze@outlook.fr', "0474117240")]
c.executemany(stmt, vals)
vals = [(2, 'murielle', 'pattyn', 'blabla', "044564615")]
c.executemany(stmt, vals)
print(request.make_request("contact_id", "contacts", "julien", None, "="))
print(c.execute(request.make_request("first_name", "contacts", "julien", None, "=")).fetchone())
print(c.execute("SELECT * FROM contacts").fetchall())
request = Request("project")
print(c.execute(request.make_request("phone", "contacts")).fetchall())
