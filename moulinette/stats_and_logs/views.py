from flask_restful import Resource

from moulinette import clientserializer, testserializer
from moulinette.stats_and_logs.models import *


class LogResource(Resource):
    def get(self):
        logs = RequestLog.query.all()
        result = []

        for log in logs:
            result.append(
                {
                    "client_id": clientserializer.dumps(log.client_id),
                    "test_id": testserializer.dumps(log.test_id),
                    "result": log.result,
                    "error": log.error,
                    "timestamp": log.created.isoformat()
                }
            )

        return {"results": result}
