from moulinette.homework.models import *

id = input()
test = Test.query.get(id)
db.session.delete(test)
db.session.commit()
