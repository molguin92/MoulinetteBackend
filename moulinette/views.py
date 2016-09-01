from moulinette import api
from moulinette.client.views import *
from moulinette.homework.views import *
from moulinette.stats_and_logs.views import *


class StaticFilesResource(Resource):
    def get(self, filename):
        return app.send_static_file('public/{fname}'.format(fname=filename))


# This file declares all the endpoints of the API.

api.add_resource(HomeworkCollectionResource, '/api/v1/homeworks',
                 '/api/v1/homeworks/')
api.add_resource(HomeworkResource, '/api/v1/homeworks/<string:hwid>')
api.add_resource(TestResource, '/api/v1/validate_tests')
api.add_resource(ClientResource, '/api/v1/clients')
api.add_resource(LogResource, '/api/v1/logs')
api.add_resource(StaticFilesResource, '/files/<string:filename>')
