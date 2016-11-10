import json
import sys

from moulinette import hwserializer
from moulinette.homework.models import *


def main():
    with open(sys.argv[1], 'r') as infile:
        hw = json.loads(infile.read())

        dbhw = Homework(hw['name'], hw['description'])
        for item in hw['items']:
            dbitem = dbhw.add_item(item['name'], item['description'])
            for test in item['tests']:
                dbtest = dbitem.add_test(test['description'], test['input'],
                                         test['output'])
                db.session.add(dbtest)
            db.session.add(dbitem)
        db.session.add(dbhw)
        db.session.commit()

    return hwserializer.dumps(dbhw.id)


if __name__ == '__main__':
    print(main())
