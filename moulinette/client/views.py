import datetime

from flask import make_response, request
from flask_restful import Resource

from moulinette import db, clientserializer, app
from moulinette.client.models import Client


class ClientResource(Resource):
    def get(self):
        client = Client()
        db.session.add(client)
        db.session.commit()

        client_id = clientserializer.dumps(client.id)

        app.logger.info(
            """
            {timestamp} Remote address {ip} requested a new client id.
                        Assigned ID {cid}
            """.format(
                timestamp=datetime.datetime.now().isoformat(),
                ip=request.remote_addr,
                cid=client_id
            )
        )

        return make_response(client_id)
