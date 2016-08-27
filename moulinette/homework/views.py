from urllib import parse

from flask_restful import Resource, reqparse, abort
from itsdangerous import URLSafeSerializer

from moulinette import app
from moulinette.homework.models import *


# This file implements al the views (endpoints) available to the homework
# model.

hwserializer = URLSafeSerializer(app.secret_key, salt="homework-salt")
itemserializer = URLSafeSerializer(app.secret_key, salt="item-salt")
testserializer = URLSafeSerializer(app.secret_key, salt="test-salt")


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
                    'input': test.stdin
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
    Endpoint for getting a specific assigment.
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
        self.post_parser.add_argument('id',
                                      type=str,
                                      required=True)
        self.post_parser.add_argument('output',
                                      type=str,
                                      required=True)

    def post(self):
        args = self.post_parser.parse_args()
        realid = testserializer.loads(args['id'])
        test = Test.query.get(realid)

        result = {
            'result_ok': True,
            'error': None
        }

        if not test:
            abort(404)

        try:
            test.validate(parse.unquote(args['output']))
        except MissingOutput:
            result['result_ok'] = False
            result['error'] = 'Missing output.'
        except ExcessiveOutput:
            result['result_ok'] = False
            result['error'] = 'Excessive output.'
        except WrongOutput:
            result['result_ok'] = False
            result['error'] = 'Wrong output.'

        return result
