from entities import *
from spjrud import *
from SyntaxTree import *

firstReq = "Select(first_name,=,julien,contacts)"
secondReq = "Project([first_name,contact_id],contacts)"
thirdReq = "Project([attr1,attr2], Re)"

db = DataBase("test.db")

arbre = SyntaxTree(secondReq,db)
arbre.display()
print(SyntaxTree.convertToSQL(arbre.root,db)[0])

