from flask_restful import Resource, reqparse, abort
from itsdangerous import BadSignature

from moulinette import hwserializer, itemserializer, testserializer, \
    clientserializer, app
from moulinette.client.models import Client
from moulinette.homework.models import *
from moulinette.stats_and_logs.models import *
import json


# This file implements al the views (endpoints) available to the homework
# model.


def serialize_homework(hw):
    """
    Unpacks a Homework object into a dictionary for easy JSON parsing.
    :param hw: A Homework item to be unpacked.
    :return: Dictionary containing the Homework along with nested Items and
    Tests.
    """
    items = []
    for item in hw.items:
        tests = []
        for test in item.tests:
            tests.append(
                {
                    'id': testserializer.dumps(test.id),
                    'description': test.description,
                    'input': test.stdin,
                    'timeout': test.timeout
                }
            )

        items.append(
            {
                'id': itemserializer.dumps(item.id),
                'name': item.name,
                'description': item.description,
                'tests': tests
            }
        )

    return {
        'id': hwserializer.dumps(hw.id),
        'name': hw.name,
        'description': hw.description,
        'items': items
    }


class HomeworkCollectionResource(Resource):
    """
    Endpoint for fetching ALL (active) homework assignments.
    """

    def get(self):
        homeworks = Homework.query.filter(Homework.active).all()
        result = []

        for hw in homeworks:
            result.append(serialize_homework(hw))

        return {'result': result}


class HomeworkResource(Resource):
    """
    Endpoint for getting a specific assignment.
    """

    def get(self, hwid):
        hw = Homework.query.get(hwserializer.loads(hwid))
        if not hw:
            abort(404)
        return serialize_homework(hw)


class TestResource(Resource):
    """
    Endpoint for validating test outputs from the client.
    """

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('client_id',
                                      type=str,
                                      required=True)
        self.post_parser.add_argument('results',
                                      type=list,
                                      required=True,
                                      location='json')

    def post(self):
        args = self.post_parser.parse_args()
        clientid = -1
        try:
            clientid = clientserializer.loads(args['client_id'])
        except BadSignature:
            abort(401)

        results = args['results']

        client = Client.query.get(clientid)
        if not client:
            abort(401)

        response = {'results': []}
        
        print('results: ' + results)

        for test in results:
            
            print('test: ' + test)

            test = json.loads(test)
            realid = testserializer.loads(test['id'])
            output = test['output']
            testdb = Test.query.get(realid)

            if not testdb:
                abort(404)

            result = {
                'test_id': test['id'],
                'result_ok': True,
                'error': ''
            }

            try:
                testdb.validate(output)
            except MissingOutput:
                result['result_ok'] = False
                result['error'] = 'Missing output.'
            except ExcessiveOutput:
                result['result_ok'] = False
                result['error'] = 'Excessive output.'
            except WrongOutput:
                result['result_ok'] = False
                result['error'] = 'Wrong output.'

            response['results'].append(result)
            log = RequestLog(realid, clientid, result['result_ok'],
                             result['error'])
            db.session.add(log)

        db.session.commit()

        app.logger.info(
            """
[{timestamp}] Client {cid} validated test results.
            """.format(
                timestamp=datetime.now().isoformat(sep=" "),
                cid=args['client_id']
            )
        )

        return response
