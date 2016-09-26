from datetime import datetime

from moulinette import db


# This file includes all the definitions for the homework model in the
# database. Any change here must then be applied to the database using the
# migrate.py file in the root folder of this project.


class Homework(db.Model):
    """
    Class Homework represents the homework table in the database.
    Contains all the information pertaining to a specific homework
    assignment, such as name, description and a list of items to be completed.
    """
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text, default='')

    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)

    items = db.relationship('Item', backref='homework')
    active = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, description=''):
        """
        Constructor for a Homework instance. Requires a name,
        and optionally, a description.
        :param name: The name of the homework assignment.
        :param description: Description of the assignment.
        """
        self.name = name
        self.description = description
        self.active = True

    def add_item(self, name, description=''):
        """
        Adds a homework item/problem/question to this homework assignment,
        and returns it for editing and chaining method calls.
        :param name: Name of the item or problem.
        :param description: Description of the item.
        :return: An Item object.
        """
        i = Item(self.id, name, description)
        db.session.add(i)
        db.session.commit()
        return i

    def activate(self):
        """
        Sets this homework to active.
        """
        self.active = True

    def deactivate(self):
        """
        Sets this homework to inactive.
        """
        self.active = False


class Item(db.Model):
    """
    Class Item represents a homework item or problem in the database.
    It contains information such as its parent homework, name, description
    and a set of tests.
    """
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, default='')

    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)

    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'),
                            nullable=False)
    tests = db.relationship('Test', backref='item')

    def __init__(self, homework_id, name, description=''):
        """
        Constructs a new Item instance, taking the parent Homework id,
        a name and optional description.
        :param homework_id: Parent Homework id.
        :param name: Name of the homework item.
        :param description: Description of the task to be accomplished.
        """
        self.name = name
        self.description = description
        self.homework_id = homework_id

    def add_test(self, description, tinput, toutput, timeout=10):
        """
        Adds a Test to this Item. Returns the Test for chaining method calls.
        :param description: Description of the new test.
        :param tinput: Input given to the program.
        :param toutput: Expected output, for verifying correctness.
        :return: A Test object.
        """
        t = Test(self.id, tinput, toutput, description, timeout=timeout)
        db.session.add(t)
        db.session.commit()
        return t


class Test(db.Model):
    """
    Class Test represents a particular test for a specific homework Item.
    Contains a reference to its parent Item object, as well as a description,
    an input to be handed to the program created by the student and an
    expected, correct output for validating the correctness of the program.
    """
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)
    timeout = db.Column(db.Integer, default=10, nullable=False)

    stdin = db.Column(db.Text)
    stdout = db.Column(db.Text)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, item_id, stdin, stdout, description='', timeout=10):
        """
        Constructs a new Test instance, taking the parent Item id, an input
        for the program to be tested and a correct output, along with an
        optional description, as parameters.
        :param item_id: Parent Item id.
        :param stdin: The input to be handed to the tested program.
        :param stdout: The expected correct output.
        :param description: Optional description of this test case.
        """
        self.item_id = item_id
        self.stdin = stdin
        self.stdout = stdout
        self.description = description
        self.timeout = timeout if timeout else 10

    def get_input_output(self):
        """
        Returns a tuple containing the input and output for this test case.
        :return: Tuple (input, output)
        """
        return self.stdin, self.stdout

    def validate(self, out):
        """
        Compares the given string to the expected correct output of this
        test case. If outputs do not match, raises one three different
        exceptions:
        Exception ExcessiveOutput: Given string is too long.
        Exception MissingOutput: Given string is too short.
        Exception WrongOutput: Lenghts match, but output does not match.
        :param out: A string to compare to the correct output.
        """

        outlines = self.stdout.strip().split("\n")
        testlines = out.strip().split("\n")

        if len(outlines) > len(testlines):
            raise ExcessiveOutput()
        elif len(outlines) < len(testlines):
            raise MissingOutput()

        for i in range(len(outlines)):
            if outlines[i] != testlines[i]:
                raise WrongOutput()


class MissingOutput(Exception):
    pass


class ExcessiveOutput(Exception):
    pass


class WrongOutput(Exception):
    pass
