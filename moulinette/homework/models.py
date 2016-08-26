from datetime import datetime

from moulinette import db


class Homework(db.Model):
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
        self.name = name
        self.description = description
        self.active = True

    def add_item(self, name, description=''):
        i = Item(self.id, name, description)
        db.session.add(i)
        db.session.commit()
        return i

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class Item(db.Model):
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
        self.name = name
        self.description = description
        self.homework_id = homework_id

    def add_test(self, description, tinput, toutput):
        t = Test(self.id, tinput, toutput, description)
        db.session.add(t)
        db.session.commit()
        return t


class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)

    stdin = db.Column(db.Text)
    stdout = db.Column(db.Text)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, item_id, stdin, stdout, description=''):
        self.item_id = item_id
        self.stdin = stdin
        self.stdout = stdout
        self.description = description

    def get_input_output(self):
        return self.stdin, self.stdout

    def validate(self, out):

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
