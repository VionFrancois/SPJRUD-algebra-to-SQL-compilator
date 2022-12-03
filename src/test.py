from request import Request
from database import DataBase

dt = DataBase("test.db")
requete = Request("Rename").make_request("contacts", "contact_id", "id")
print(requete)
dt.execute(requete, "contacts")
requet2 = Request("Project").make_request("contacts", "id")
print(requet2)
print(Request("Union").make_request(requet2, None, None, requete))
dt.execute(Request("Difference").make_request(requete, None, None, requet2),"contacts")

print(dt.display())