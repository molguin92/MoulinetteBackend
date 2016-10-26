from moulinette import hwserializer
from moulinette.homework.models import *
from moulinette.stats_and_logs.models import *


def get_submissions_hw(id):
    count = 0
    items = Item.query.filter(Item.homework_id == id).all()
    for item in items:
        tests = Test.query.filter(Test.item_id == item.id).all()
        for test in tests:
            submissions = RequestLog.query.filter(RequestLog.test_id ==
                                                  test.id).all()
            count += len(submissions)

    return count


if __name__ == '__main__':
    homeworks = Homework.query.all()
    for homework in homeworks:
        serialid = hwserializer.dumps(homework.id)
        print('ID: ' + serialid)
        print('Name: ' + homework.name)
        print('Count: ' + str(get_submissions_hw(homework.id)))
        print()
