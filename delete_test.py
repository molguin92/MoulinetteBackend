from moulinette import testserializer
from moulinette.homework.models import *

id = input()

test = Test.query.get(testserializer.loads(id))
db.session.delete(test)
db.session.commit()
