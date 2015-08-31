from moulinette import db
from datetime import datetime

class TestCase ( db.Model ):
    __tablename__ = 'testcase'
    id = db.Column ( db.Integer, primary_key = True )
    problem_id = db.Column ( db.Integer, db.ForeignKey('problem.id'), nullable = False )

    input = db.Column ( db.String )
    output = db.Column ( db.String, nullable = False )

    created = db.Column ( db.DateTime, nullable = False, default = datetime.now() )
    updated = db.Column ( db.DateTime, nullable = False, default = datetime.now(), onupdate = datetime.now() )
