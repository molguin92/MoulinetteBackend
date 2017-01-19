import csv
import os
import tempfile
from datetime import timedelta, date as ddate
from io import BytesIO

from flask import send_file
from flask_restful import Resource, reqparse
from sqlalchemy.util import OrderedDict

from moulinette import clientserializer, testserializer
from moulinette.stats_and_logs.models import *


class LogResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('summary', type=bool, default=False,
                                 required=False)
        self.parser.add_argument('csv', type=bool, default=False,
                                 required=False)

    def get(self):
        args = self.parser.parse_args()
        if args.get('summary'):
            logs = RequestLog.query.order_by(RequestLog.created).all()

            if len(logs) < 1:
                return {}

            first_d = logs[0].created.date()
            last_d = logs[-1].created.date()

            result = OrderedDict()

            t_date = ddate(first_d.year, first_d.month, first_d.day)
            while t_date != last_d:
                result[str(t_date)] = 0
                t_date += timedelta(days=1)

            for log in logs:
                date = log.created.date()
                sdate = str(date)
                if result.get(sdate):
                    result[sdate] += 1
                else:
                    result[sdate] = 1

            if args.get('csv'):
                csv_tmp = tempfile.NamedTemporaryFile(mode='w+',
                                                      prefix='logs_csv_',
                                                      delete=False)
                csv_writer = csv.writer(csv_tmp)
                csv_writer.writerow(['DATE', 'N_REQUESTS'])

                for k, v in result.items():
                    csv_writer.writerow([k, v])

                csv_tmp.close()

                tmp_send = BytesIO()
                with open(csv_tmp.name, mode='rb') as f:
                    tmp_send.write(f.read())

                tmp_send.seek(0)
                response = send_file(tmp_send, mimetype='text/csv',
                                     as_attachment=True,
                                     attachment_filename='logs.csv')

                os.remove(csv_tmp.name)
                return response

            else:
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
