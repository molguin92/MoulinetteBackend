from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#app.secret_key = b':\x8f\x89~%p\x8e4\x0e\xefg\xe8,\x9a\xa7\x9f5\x82\xfc\x0flN\xeeI'
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
