import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

from moulinette.homework.models import *
import moulinette.views

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
