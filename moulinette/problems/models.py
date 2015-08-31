from moulinette import db
from datetime import datetime

class Problem ( db.Model ):
    __tablename__ = 'problem'
    id = db.Column ( db.Integer, primary_key = True )
    name = db.Column ( db.String, unique = True, index = True )
    description = db.Column ( db.Text )
    example_in = db.Column ( db.Text )
    example_out = db.Column ( db.Text )

    test_cases = db.relationship ( 'TestCase', backref = 'problem', lazy = 'dynamic' )
    submissions = db.relationship ( 'Submission', backref = 'problem', lazy = 'dynamic' )
    stats = db.relationship ( 'ProblemStats', backref = 'problem', lazy = 'dynamic' )

    created = db.Column ( db.DateTime, nullable = False, default = datetime.now() )
    updated = db.Column ( db.DateTime, nullable = False, default = datetime.now(), onupdate = datetime.now() )

    #Future: Course

    def __init__(self, name, description = '', example_in = '', example_out = ''):
        self.name = name
        self.description = description
        self.example_in = example_in
        self.example_out = example_out



