from flask_restful import Resource, reqparse, abort
from moulinette.homework.models import *
from moulinette import app
from itsdangerous import URLSafeSerializer


class HomeworkCollectionResource(Resource):
    def __init__(self):
        self.serializer = URLSafeSerializer(app.config['SECRET_KEY'])

    def get(self):
        homeworks = Homework.query.filter(Homework.active).all()
        result = []

        for hw in homeworks:
            result.append({
                'id': self.serializer.dumps(hw.id),
                'name': hw.name,
                'description': hw.description
            })

        return {'len': len(result),
                'result': result}


class HomeworkResource(Resource):
    def __init__(self):
        self.serializer = URLSafeSerializer(app.config['SECRET_KEY'])

    def get(self, hwid):
        hw = Homework.query.get(self.serializer.loads(hwid))
        if not hw:
            abort(404)
        return self.serialize_homework(hw)

    def serialize_homework(self, hw):
        items = []
        for item in hw.items:
            tests = []
            for test in item.tests:
                tests.append(
                    {
                        'id': self.serializer.dumps(test.id),
                        'input': test.stdin
                    }
                )

            items.append(
                {
                    'id': self.serializer.dumps(item.id),
                    'name': item.name,
                    'description': item.description,
                    'tests': tests
                }
            )

        return {
            'id': self.serializer.dumps(hw.id),
            'name': hw.name,
            'description': hw.description,
            'items': items
        }


class TestResource(Resource):
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
        test = Test.query.get(args['id'])

        result = {
            'result_ok': True,
            'error': None
        }

        if not test:
            abort(404)

        try:
            test.validate(args['output'])
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
