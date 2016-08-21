from flask_restful import Resource, reqparse, abort
from moulinette.homework.models import *


def serializeHomework(hw):
    items = []
    for item in hw.items:
        tests = []
        for test in item.tests:
            tests.append(
                {
                    'id': test.id,
                    'input': test.stdin
                }
            )

        items.append(
            {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'tests': tests
            }
        )

    return {
        'id': hw.id,
        'name': hw.name,
        'description': hw.description,
        'items': items
    }



class HomeworkResource(Resource):
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('id',
                                     type=int,
                                     required=False)

    def get(self):
        args = self.get_parser.parse_args()
        hwid = args.get('id', False)
        if hwid:
            return self.gethw(hwid)
        else:
            return self.getall()

    def gethw(self, hwid):
        hw = Homework.query.get(hwid)
        if not hw:
            return {'error': 'No homework with id ' + hwid}, 404
        return serializeHomework(hw)



    def getall(self):
        homeworks = Homework.query.filter(Homework.active).all()
        result = []

        for hw in homeworks:
            result.append({
                'id': hw.id,
                'name': hw.name,
                'description': hw.description
            })

        return {'len': len(result),
                'result': result}


class ItemResource(Resource):
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('id',
                                     type=int,
                                     required=True)

    def get(self):
        args = self.get_parser.parse_args()
        items = Homework.query.get(args['id']).items
        result = []

        for item in items:
            result.append({
                'id': item.id,
                'name': item.name,
                'description': item.description
            })

        return {'len': len(result),
                'result': result}


class TestResource(Resource):
    def __init__(self):
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('id',
                                     type=int,
                                     required=True)

        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('id',
                                      type=int,
                                      required=True)
        self.post_parser.add_argument('output',
                                      type=str,
                                      required=True)

    def get(self):
        args = self.get_parser.parse_args()
        tests = Item.query.get(args['id']).tests
        result = []

        for test in tests:
            result.append({
                'id': test.id,
                'input': test.stdin
            })

        return {'len': len(result),
                'result': result}

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
