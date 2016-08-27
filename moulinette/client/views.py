from flask_restful import Resource
from itsdangerous import URLSafeSerializer

from moulinette import db, app
from moulinette.client.models import Client


class ClientResource(Resource):
    def get(self):
        client = Client()
        db.session.add(client)
        db.session.commit()
        return URLSafeSerializer(app.config['SECRET_KEY'],
                                 salt="client-salt").dumps(client.id)
