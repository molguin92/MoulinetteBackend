import click

from moulinette import hwserializer
from moulinette.homework.models import *

if __name__ == '__main__':
    hwid = click.prompt('HW to fix:', type=str)
    hwid = hwserializer.loads(hwid)

    items = Item.query.filter(Item.homework_id == hwid).all()
    for item in items:
        tests = Test.query.filter(Test.item_id == item.id).all()
        for test in tests:
            test.stdin = test.stdin.replace(',', '')
            test.stdout = test.stdout.replace(',', '')
            db.session.add(test)

        db.session.add(item)

    db.session.commit()
    click.echo('Done!')
