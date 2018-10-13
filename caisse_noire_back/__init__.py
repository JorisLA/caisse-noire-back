import uuid
import sqlite3
import os
import jwt
import datetime
from flask import Flask, jsonify, request, g, session, make_response
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from functools import wraps

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sqlite3.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))
# enable CORS
CORS(app)
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
            current_user = query_db('SELECT * FROM players WHERE uuid = ?',
                [
                    data['public_id']
                ],
                one=True,
            )
            kwargs['current_user'] = current_user
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


import caisse_noire_back.players.views
import caisse_noire_back.fines.views
import caisse_noire_back.players_fines.views
import caisse_noire_back.login.views
import caisse_noire_back.teams.views

if __name__ == '__main__':
    app.run()

