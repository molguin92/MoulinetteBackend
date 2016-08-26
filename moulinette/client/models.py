from datetime import datetime

from moulinette import db


class Client(db.Model):
    """
    Class Client represents a remote client associated with this server.
    Whenever a new client connects, a corresponding entry in the DB is
    created and the ID transmitted to the client.
    """
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)
