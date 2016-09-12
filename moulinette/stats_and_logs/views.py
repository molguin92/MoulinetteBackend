from datetime import timedelta

from flask_restful import Resource

from moulinette import clientserializer, testserializer
from moulinette.stats_and_logs.models import *


class LogResource(Resource):
    def get(self):
        startdate = datetime.today().date() - timedelta(days=7)
        print(startdate)
        logs = RequestLog.query.filter(
            RequestLog.created > startdate
        ).all()
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

        print(startdate.isoformat())
        return {"results": result, "startdate": startdate.isoformat()}
