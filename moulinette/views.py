from moulinette.homework.views import *
from moulinette import api

api.add_resource(HomeworkCollectionResource, '/api/v1/homeworks',
                 '/api/v1/homeworks/')
api.add_resource(HomeworkResource, '/api/v1/homeworks/<string:hwid>')
api.add_resource(TestResource, '/api/v1/validate_test')
