from flask_restful import Resource, reqparse, abort
from moulinette.homework.models import *


class HomeworkResource(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('test_id',
                                      type=int,
                                      required=True)
        self.post_parser.add_argument('output',
                                      type=str,
                                      required=True)

    def get(self):
        homeworks = Homework.query.filter(Homework.active).all()
        result = []

        for hw in homeworks:
            result.append({
                'id': hw.id,
                'name': hw.name,
                'description': hw.description,
                'items': len(hw.items)
            })

        return {'len': len(result),
                'result': result}

    def post(self):
        args = self.post_parser.parse_args()
        test = Test.query.get(args['test_id'])

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



