import click
from itsdangerous import URLSafeSerializer

from moulinette import app
from moulinette.homework.models import *

serializer = URLSafeSerializer(app.config['SECRET_KEY'])


def startup():
    value = click.prompt(
        'Please select an action:\n'
        '1. Create a homework assignment.\n'
        '2. Deactivate a homework assignment.\n'
        '3. Reactivate a homework assignment.\n'
        '4. Delete a homework assignment.\n'
        '5. List active homework assignments.\n'
        '6. List ALL homework assignments.\n'
        '0. Exit.\n>> ', default=0, type=int, show_default=False)

    click.echo('\n')

    if value == 1:
        create_hw()
    elif value == 2:
        deactivate_hw()
    elif value == 4:
        delete_hw()
    elif value == 5:
        list_active()
    elif value == 6:
        list_all()
    else:
        exit()


def create_hw():
    name = click.prompt('Name of the assignment', type=str)
    description = click.prompt('Description', type=str)

    hw = Homework(name, description)
    db.session.add(hw)
    db.session.commit()

    click.echo('Homework created with id: ' + serializer.dumps(hw.id))
    additem = click.confirm('Do you wish to add an item to this homework?')
    while additem:
        add_item_to_homework(hw)
        additem = click.confirm('Do you wish to add another item?')


def add_item_to_homework(hw):
    name = click.prompt('Name of the homework item', type=str)
    description = click.prompt('Description', type=str)

    item = hw.add_item(name, description)
    click.echo('Created item with id: ' + serializer.dumps(item.id))
    addtest = click.confirm('Do you wish to add a test to this item?')
    while addtest:
        add_test_to_item(item)
        addtest = click.confirm('Do you wish to add another test?')


def add_test_to_item(item):
    stdin = click.prompt('INPUT', type=str)
    stdout = click.prompt('OUTPUT', type=str)

    t = item.add_test(stdin, stdout)
    click.echo('Created test with id: ' + serializer.dumps(t.id))


def deactivate_hw():
    id = click.prompt('ID of the homework to deactivate', type=str)
    realid = serializer.loads(id)
    hw = Homework.query.get(realid)
    if hw:
        hw.deactivate()
        db.session.commit()
        click.echo('Deactivated homework: ' + serializer.dumps(hw.id))
    else:
        click.echo('No such homework: ' + id)


def delete_hw():
    id = click.prompt('ID of the homework to delete', type=str)
    realid = serializer.loads(id)
    hw = Homework.query.get(realid)
    if hw:
        if not click.confirm('Please confirm!', default=False):
            return

        for item in hw.items:
            for test in item.tests:
                db.session.delete(test)

            db.session.delete(item)
        db.session.delete(hw)
        db.session.commit()
        click.echo('Deleted homework: ' + serializer.dumps(hw.id))
    else:
        click.echo('No such homework: ' + id)


def list_active():
    active = Homework.query.filter(Homework.active).all()
    click.echo('Active assigments: (id - name)')
    for hw in active:
        click.echo(serializer.dumps(hw.id) + ' - ' + hw.name)
    click.echo('\n')


def list_all():
    active = Homework.query.all()
    click.echo('Assigments: (id - name)')
    for hw in active:
        click.echo(serializer.dumps(hw.id) + ' - ' + hw.name)
    click.echo('\n')


if __name__ == '__main__':
    while True:
        startup()
