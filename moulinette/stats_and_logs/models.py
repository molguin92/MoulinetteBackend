from datetime import datetime

from moulinette import db


class RequestLog(db.Model):
    __tablename__ = 'requestlog'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)

    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'),
                          nullable=False)
    result = db.Column(db.Boolean, nullable=False)
    error = db.Column(db.String)

    def __init__(self, test_id, client_id, result, error=None):
        self.test_id = test_id
        self.client_id = client_id
        self.result = result
        self.error = error
