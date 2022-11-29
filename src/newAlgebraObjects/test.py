from request import Request
from database import DataBase
import sqlite3

dt = DataBase("test.db")
dt.execute(Request("project").make_request("*", "contacts"),"contacts")
print(dt.display())