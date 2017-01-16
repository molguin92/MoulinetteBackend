from datetime import timedelta

from flask_restful import Resource, reqparse
from sqlalchemy.util import OrderedDict

from moulinette import clientserializer, testserializer
from moulinette.stats_and_logs.models import *


class LogResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('summary', type=bool, default=False,
                                 required=False)

    def get(self):
        args = self.parser.parse_args()
        if args.get('summary'):
            logs = RequestLog.query.order_by(RequestLog.created).all()

            if len(logs) < 1:
                return {}

            result = OrderedDict()
            prev_date = logs[0].created.date()

            for log in logs:
                date = log.created.date()

                if date > prev_date:
                    new_date = date + timedelta(days=1)
                    while new_date < date:
                        result[str(new_date)] = 0
                        new_date = date + timedelta(days=1)

                sdate = str(date)
                if result.get(sdate):
                    result[sdate] += 1
                else:
                    result[sdate] = 1

                prev_date = date

            return result

        else:
            startdate = datetime.today().date() - timedelta(days=7)
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

            return {"results": result, "startdate": startdate.isoformat()}
