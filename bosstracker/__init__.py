from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from bosstracker.config import Config


app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '0e17b29abff7ec5d85cac7d1f48f28d3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

from bosstracker import routes

