import flask
from flask_restful import Resource
from itsdangerous import URLSafeSerializer

from moulinette import db, app
from moulinette.client.models import Client

clientserializer = URLSafeSerializer(app.secret_key, salt="client-salt")


class ClientResource(Resource):
    def get(self):
        client = Client()
        db.session.add(client)
        db.session.commit()

        return flask.make_response(clientserializer.dumps(client.id))
