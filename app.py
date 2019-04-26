import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from common.json_encoder import JSONSerializer


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SENDGRID_API_KEY'] = os.environ.get('SENDGRID_API_KEY')
    app.config['SENDGRID_DEFAULT_FROM'] = 'admin@caissenoire.com'

    db = SQLAlchemy()
    db.init_app(app)

    # enable CORS
    cors = CORS(app)

    from views.players.views import PlayerApi
    app.add_url_rule('/players', view_func=PlayerApi.as_view('players'))
    app.add_url_rule('/players/<player_uuid>', view_func=PlayerApi.as_view('player'))
    from views.fines.views import FineApi
    app.add_url_rule('/fines', view_func=FineApi.as_view('fines'))
    app.add_url_rule('/fines/<fine_uuid>', view_func=FineApi.as_view('fine'))
    from views.players_fines.views import BillApi, mail
    mail.init_app(app)
    app.add_url_rule('/bills', view_func=BillApi.as_view('bills'))
    app.add_url_rule('/bills/<player_uuid>', view_func=BillApi.as_view('bill'))
    from views.signin.views import SigninApi, bcrypt
    bcrypt.init_app(app)
    app.add_url_rule('/signin', view_func=SigninApi.as_view('signin'))
    from views.signup.views import SignupApi, bcrypt
    bcrypt.init_app(app)
    app.add_url_rule('/signup', view_func=SignupApi.as_view('signup'))
    from views.statistics.views import StatisticApi
    app.add_url_rule('/statistic', view_func=StatisticApi.as_view('statistics'))
    from views.teams.views import TeamApi
    app.add_url_rule('/teams', view_func=TeamApi.as_view('teams'))

    return app

if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    create_app()
    # app.run()
