import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
db = SQLAlchemy(app)
api = Api(app)

from moulinette.homework import models
import moulinette.views

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
