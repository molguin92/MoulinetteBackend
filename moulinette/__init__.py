import logging
import os
from logging.handlers import RotatingFileHandler

from flask import render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeSerializer

from moulinette.flask_ext import *

app = ExtFlask(__name__)
app.config['APPLICATION_ROOT'] = os.environ.get('APP_ROOT', False)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.logger.addHandler(RotatingFileHandler('.moulinette.log',
                                          maxBytes=5242880,  # 5 MiB
                                          backupCount=3))
app.logger.setLevel(logging.INFO)

db = SQLAlchemy(app, use_native_unicode=False)
api = Api(app)

hwserializer = URLSafeSerializer(app.secret_key, salt="homework-salt")
itemserializer = URLSafeSerializer(app.secret_key, salt="item-salt")
testserializer = URLSafeSerializer(app.secret_key, salt="test-salt")
clientserializer = URLSafeSerializer(app.secret_key, salt="client-salt")

from moulinette.homework import models
import moulinette.views


@app.route('/')
def home():
    return app.send_static_file("index.html")


@app.route('/stats')
def test():
    url = '/api/v1/logs'
    if app.config.get('APPLICATION_ROOT', False):
        url = app.config['APPLICATION_ROOT'] + url

    return render_template('d3vis.html', url=url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
