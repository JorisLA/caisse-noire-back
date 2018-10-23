import uuid
import sqlite3
import os
import jwt
import datetime
from flask import Flask, jsonify, request, g, session, make_response
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_sendgrid import SendGrid
from sqlalchemy import func
from functools import wraps
from sqlalchemy.sql import text

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SENDGRID_API_KEY'] = 'your api key'
app.config['SENDGRID_DEFAULT_FROM'] = 'admin@yourdomain.com'
mail = SendGrid(app)
db = SQLAlchemy(app)
from models import Player, Fine, Team, PlayerFines, TeamFines
# enable CORS
cors = CORS(app)
# enable Bcrypt for password encryption
bcrypt = Bcrypt(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Player.query.filter_by(uuid=data['public_id']).first()
            kwargs['current_user'] = current_user
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated

import players.views
import fines.views
import players_fines.views
import login.views
import teams.views

if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    app.run()

