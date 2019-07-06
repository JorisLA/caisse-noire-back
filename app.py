import os

from flask_sendgrid import SendGrid
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask

from database import db
from caisse_noire.common.json_encoder import JSONSerializer

# db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
mail = SendGrid()


def create_app():
    from caisse_noire.api.v1.ping.ping import PingHandler
    from caisse_noire.api.v1.teams.teams import TeamsHandler
    from caisse_noire.api.v1.statistics.statistics import StatisticsHandler
    from caisse_noire.api.v1.players.signup import SignupHandler
    from caisse_noire.api.v1.players.signin import SigninHandler
    from caisse_noire.api.v1.fines.fine import FineHandler
    from caisse_noire.api.v1.fines.fines import FinesHandler
    from caisse_noire.api.v1.players.fine import PlayerFineHandler
    from caisse_noire.api.v1.players.fines import PlayersFinesHandler
    from caisse_noire.api.v1.players.player import PlayerHandler
    from caisse_noire.api.v1.players.players import PlayersHandler
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # routes
    app.add_url_rule('/players', view_func=PlayersHandler.as_view('players'))
    app.add_url_rule('/players/<player_uuid>',
                     view_func=PlayerHandler.as_view('player'))
    app.add_url_rule('/players/fines',
                     view_func=PlayersFinesHandler.as_view('players_fines'))
    app.add_url_rule('/players/<player_uuid>/fine',
                     view_func=PlayerFineHandler.as_view('player_fine'))
    app.add_url_rule('/fines', view_func=FinesHandler.as_view('fines'))
    app.add_url_rule('/fines/<fine_uuid>',
                     view_func=FineHandler.as_view('fine'))
    app.add_url_rule('/players/signin',
                     view_func=SigninHandler.as_view('player_signin'))
    app.add_url_rule('/players/signup',
                     view_func=SignupHandler.as_view('player_signup'))
    app.add_url_rule(
        '/statistics', view_func=StatisticsHandler.as_view('statistics'))
    app.add_url_rule('/teams', view_func=TeamsHandler.as_view('teams'))
    # Health check
    app.add_url_rule('/ping', view_func=PingHandler.as_view('ping'))

    return app
