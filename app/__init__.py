from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from app import views, models