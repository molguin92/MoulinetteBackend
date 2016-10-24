from random import random

import click

from max_subarray import get_output
from moulinette import hwserializer
from moulinette.homework.models import *


def generate_array(length, min_val, max_val):
    result = []
    for i in range(length):
        result.append(random.randint(min_val, max_val))
    return result


def is_negative(l):
    for item in l:
        if int(item) >= 0:
            return False

    return True


if __name__ == '__main__':
    hwid = click.prompt('HW to fix:', type=str)
    hwid = hwserializer.loads(hwid)

    items = Item.query.filter(Item.homework_id == hwid).all()
    for item in items:
        tests = Test.query.filter(Test.item_id == item.id).all()
        for test in tests:
            lstdout = test.stdout.strip().split('\n')
            for i in range(len(lstdout)):
                line = lstdout[i]
                linel = line.split(' ')
                while is_negative(linel):
                    A = generate_array(len(linel), random.randint(-500, 0),
                                       random.randint(0, 500))
                    line = str(A)[1:len(A) - 1].replace(',', '')
                    linel = line.split(' ')
                lstdout[i] = line

            test.stdin = '\n'.join(lstdout)
            test.stdout = get_output(test.stdin)
            test.timeout = 600
            db.session.add(test)

        db.session.add(item)

    db.session.commit()
    click.echo('Done!')
