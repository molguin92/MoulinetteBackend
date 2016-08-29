import flask
from flask_restful import Resource

from moulinette import db
from moulinette.client.models import Client


class ClientResource(Resource):
    def get(self):
        client = Client()
        db.session.add(client)
        db.session.commit()

        return flask.make_response(clientserializer.dumps(client.id))
