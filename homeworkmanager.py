import sys

import click

from moulinette import hwserializer, itemserializer, testserializer
from moulinette.homework.models import *


def startup():
    value = click.prompt(
        'Please select an action:\n'
        '1. Create a homework assignment.\n'
        '2. Edit a homework assignment.\n'
        '3. Edit a homework item.\n'
        '4. Deactivate a homework assignment.\n'
        '5. Reactivate a homework assignment.\n'
        '6. Delete a homework assignment.\n'
        '7. List active homework assignments.\n'
        '8. List ALL homework assignments.\n'
        '9. Fix all tests with null timeout.\n'
        '0. Exit.\n>> ', default=0, type=int, show_default=False)

    click.echo('\n')

    if value == 1:
        create_hw()
    elif value == 2:
        edit_hw()
    elif value == 3:
        edit_item()
    elif value == 4:
        deactivate_hw()
    elif value == 5:
        pass
    elif value == 6:
        delete_hw()
    elif value == 7:
        list_active()
    elif value == 8:
        list_all()
    elif value == 9:
        fix_tests_timeout()
    else:
        exit()


def fix_tests_timeout():
    tests = Test.query.all()
    for test in tests:
        if not test.timeout:
            test.timeout = 10
            db.session.add(test)
            db.session.commit()


def create_hw():
    name = click.prompt('Name of the assignment', type=str)
    click.echo('Description: (Ctrl-D to finish):')
    description = sys.stdin.read()

    hw = Homework(name, description)
    db.session.add(hw)
    db.session.commit()

    click.echo('Homework created with id: ' + hwserializer.dumps(hw.id))
    additem = click.confirm('Do you wish to add an item to this homework?')
    while additem:
        add_item_to_homework(hw)
        additem = click.confirm('Do you wish to add another item?')


def edit_hw():
    id = click.prompt('ID of homework to edit: ', type=str)
    hw = Homework.query.get(hwserializer.loads(id))

    click.echo("Homework name: " + hw.name)
    click.echo("Homework description: " + hw.description)

    if click.confirm('Change name?', default=True):
        name = click.prompt('New name: ', type=str)
        hw.name = name

    if click.confirm('Change description?', default=True):
        click.echo('New description: (Ctrl-D to finish):')
        description = sys.stdin.read()
        hw.description = description

    db.session.add(hw)
    db.session.commit()


def edit_item():
    id = click.prompt('ID of item to edit: ', type=str)
    item = Item.query.get(itemserializer.loads(id))

    click.echo("Item name: " + item.name)
    click.echo("Item description: " + item.description)

    if click.confirm('Change name?', default=True):
        name = click.prompt('New name: ', type=str)
        item.name = name

    if click.confirm('Change description?', default=True):
        click.echo('New description: (Ctrl-D to finish):')
        description = sys.stdin.read()
        item.description = description

    db.session.add(item)
    db.session.commit()


def add_item_to_homework(hw):
    name = click.prompt('Name of the homework item', type=str)
    click.echo('Description: (Ctrl-D to finish):')
    description = sys.stdin.read()

    item = hw.add_item(name, description)
    click.echo('Created item with id: ' + itemserializer.dumps(item.id))
    addtest = click.confirm('Do you wish to add a test to this item?')
    while addtest:
        add_test_to_item(item)
        addtest = click.confirm('Do you wish to add another test?')


def getTestInOut():
    click.echo('Enter test input (Ctrl-D to finish):')
    stdin = sys.stdin.read()
    click.echo('Enter test output (Ctrl-D to finish):')
    stdout = sys.stdin.read()
    return stdin, stdout


def add_test_to_item(item):
    stdin, stdout = '', ''
    description = click.prompt('Description')
    timeout = click.prompt('Timeout (in seconds)', type=int, default=10)
    if click.confirm("Get input and output from files?", default=False):
        while True:
            infname = click.prompt('Path to input file')
            outfname = click.prompt('Path to output file')
            with open(infname, 'r') as infile, open(outfname, 'r') as outfile:
                stdin = infile.read()
                stdout = outfile.read()

                click.echo('\nTest input:\n')
                click.echo(stdin)
                click.echo('\nTest output:\n')
                click.echo(stdout)

                if click.confirm('\nIs this correct?', default=True):
                    break
    else:
        while True:
            stdin, stdout = getTestInOut()
            click.echo('\nTest input:\n')
            click.echo(stdin)
            click.echo('\nTest output:\n')
            click.echo(stdout)

            if click.confirm('\nIs this correct?', default=True):
                break

    t = item.add_test(description, stdin, stdout, timeout=timeout)
    click.echo('Created test with id: ' + testserializer.dumps(t.id))


def deactivate_hw():
    id = click.prompt('ID of the homework to deactivate', type=str)
    realid = hwserializer.loads(id)
    hw = Homework.query.get(realid)
    if hw:
        hw.deactivate()
        db.session.commit()
        click.echo('Deactivated homework: ' + hwserializer.dumps(hw.id))
    else:
        click.echo('No such homework: ' + id)


def delete_hw():
    id = click.prompt('ID of the homework to delete', type=str)
    realid = hwserializer.loads(id)
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
        click.echo('Deleted homework: ' + hwserializer.dumps(hw.id))
    else:
        click.echo('No such homework: ' + id)


def list_active():
    active = Homework.query.filter(Homework.active).all()
    click.echo('Active assigments: (id - name)')
    for hw in active:
        click.echo(hwserializer.dumps(hw.id) + ' - ' + hw.name)
    click.echo('\n')


def list_all():
    active = Homework.query.all()
    click.echo('Assigments: (id - name)')
    for hw in active:
        click.echo(hwserializer.dumps(hw.id) + ' - ' + hw.name)
    click.echo('\n')


if __name__ == '__main__':
    while True:
        startup()
