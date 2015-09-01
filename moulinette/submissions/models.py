from moulinette import db
from datetime import datetime

class Submission ( db.Model ):
    __tablename__ = 'submission'
    id = db.Column ( db.Integer, primary_key = True )
    problem_id = db.Column ( db.Integer, db.ForeignKey ( 'problem.id' ) )

    code = db.Column ( db.String, nullable = False )