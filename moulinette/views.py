from moulinette.homework.views import *
from moulinette import api

api.add_resource(HomeworkResource, '/api/v1/homeworks')
api.add_resource(ItemResource, '/api/v1/items')
api.add_resource(TestResource, '/api/v1/tests')
