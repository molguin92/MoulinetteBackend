import click

from moulinette.homework.models import *


def startup():
    value = click.prompt(
        'Please select an action:\n'
        '1. Create a homework assignment.\n'
        '2. Deactivate a homework assignment.\n'
        '3. Delete a homework assignment.\n'
        '4. List active homework assignments.\n'
        '5. List ALL homework assignments.\n'
        '0. Exit.\n>> ', default=0, type=int, show_default=False)

    click.echo('\n')

    if value == 1:
        create_hw()
    elif value == 2:
        deactivate_hw()
    elif value == 3:
        print('delete')
    elif value == 4:
        list_active()
    elif value == 5:
        list_all()
    else:
        exit()


def create_hw():
    name = click.prompt('Name of the assignment', type=str)
    description = click.prompt('Description', type=str)

    hw = Homework(name, description)
    db.session.add(hw)
    db.session.commit()

    click.echo('Homework created with id' + str(hw.id))
    additem = click.confirm('Do you wish to add an item to this homework?')
    while additem:
        add_item_to_homework(hw)
        additem = click.confirm('Do you wish to add another item?')


def add_item_to_homework(hw):
    name = click.prompt('Name of the homework item', type=str)
    description = click.prompt('Description', type=str)

    item = hw.add_item(name, description)
    click.echo('Created item with id: ' + str(item.id))
    addtest = click.confirm('Do you wish to add a test to this item?')
    while addtest:
        add_test_to_item(item)
        addtest = click.confirm('Do you wish to add another test?')


def add_test_to_item(item):
    stdin = click.prompt('INPUT', type=str)
    stdout = click.prompt('OUTPUT', type=str)

    t = item.add_test(stdin, stdout)
    click.echo('Created test with id: ' + str(t.id))


def deactivate_hw():
    id = click.prompt('ID of the homework to deactivate', type=int)
    hw = Homework.query.get(id)
    if hw:
        hw.deactivate()
        db.session.commit()
        click.echo('Deactivated homework: ' + str(hw.id))
    else:
        click.echo('No such homework: ' + str(id))


def list_active():
    active = Homework.query.filter(Homework.active).all()
    click.echo('Active assigments: (id - name)')
    for hw in active:
        click.echo(str(hw.id) + ' - ' + hw.name)
    click.echo('\n')


def list_all():
    active = Homework.query.all()
    click.echo('Assigments: (id - name)')
    for hw in active:
        click.echo(str(hw.id) + ' - ' + hw.name)
    click.echo('\n')


if __name__ == '__main__':
    while True:
        startup()
