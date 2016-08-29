import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# Main application file.
# From here we set up the Flask application framework, and initialize
# the global configuration variables.

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = os.environ['APP_ROOT']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

from moulinette.homework import models
import moulinette.views


@app.route('/')
def home():
    return "It works! Welcome to the Moulinette API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
