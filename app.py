import sqlite3
import os

from flask import Flask, jsonify, request, g, session, make_response
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_sendgrid import SendGrid
from sqlalchemy import func, exc
from functools import wraps
from sqlalchemy.sql import text

from common.json_encoder import JSONSerializer

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SENDGRID_API_KEY'] = os.environ.get('SENDGRID_API_KEY')
app.config['SENDGRID_DEFAULT_FROM'] = 'admin@caissenoire.com'
""" app.json_encoder = JSONSerializer """
""" app.config['SQLALCHEMY_ECHO'] = True """
mail = SendGrid(app)
db = SQLAlchemy(app)
from models.player import Player, PlayerFines
from models.team import Team, TeamFines
from models.fine import Fine
# enable CORS
cors = CORS(app)
# enable Bcrypt for password encryption
bcrypt = Bcrypt(app)

import views.players.views
import views.fines.views
import views.players_fines.views
import views.signin.views
import views.signup.views
import views.teams.views
import views.statistics.views

if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    app.run()

