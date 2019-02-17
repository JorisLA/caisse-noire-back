import uuid
import pytest
import jwt
import datetime

from app import (
    Flask,
    os,
    db,
    bcrypt,
    Player,
    Team
)
from models.repository.fine_repository import FineModelRepository
from models.repository.player_repository import PlayerModelRepository
from models.repository.team_repository import TeamModelRepository
from views.players.views import PlayerApi
from views.fines.views import FineApi
from views.players_fines.views import BillApi
from views.signin.views import SigninApi
from views.signup.views import SignupApi
from views.teams.views import TeamApi
from views.statistics.views import StatisticApi


class Client():
    """
    Every Client object should inherit from this class in order to prossess
    a proper authentication method.
    """
    def __init__(self):
        self.app_test = Flask(__name__)
        self.test_client = self.app_test.test_client()
        self.app_test.config.from_object(os.environ['APP_SETTINGS'])
        # Flask provides a way to test your application by exposing the Werkzeug test Client
        # and handling the context locals for you.
        self.app_test.add_url_rule('/players', view_func=PlayerApi.as_view('players'))
        self.app_test.add_url_rule('/players/<player_uuid>', view_func=PlayerApi.as_view('player'))
        self.app_test.add_url_rule('/signin', view_func=SigninApi.as_view('signin'))
        self.app_test.add_url_rule('/fines', view_func=FineApi.as_view('fines'))
        self.app_test.add_url_rule('/fines/<fine_uuid>', view_func=FineApi.as_view('fine'))
        self.app_test.add_url_rule('/bills', view_func=BillApi.as_view('bills'))
        self.app_test.add_url_rule('/bills/<player_uuid>', view_func=BillApi.as_view('bill'))
        self.app_test.add_url_rule('/signup', view_func=SignupApi.as_view('signup'))
        # Establish an application context before running the tests.
        self.ctx = self.app_test.app_context()

        self.ctx.push()

        db.init_app(self.app_test)
        db.create_all()


class AdminClient(Client):
    """
    """
    def __init__(self):
        super().__init__()
        self.pw_hash = bcrypt.generate_password_hash('thisismypassword')
        self.team_name = 'Dummy team name'
        self.player_info = {
            'first_name':'player first name',
            'last_name':'player last name',
            'email':'player@gmail.com',
            'pw_hash':self.pw_hash,            
        }
        self.token = ''
        self.team_uuid = TeamModelRepository.create_team(self,team_name=self.team_name)

    def bankerClient(self):
        self.player_info['team_uuid'] = self.team_uuid
        self.player_info['banker'] = True
        self.player_uuid = PlayerModelRepository.create_player(self, player_info=self.player_info)
        self.token = jwt.encode(
            {
                'public_id' : self.player_uuid,
                'team_uuid' : self.team_uuid,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            },
            self.app_test.config['SECRET_KEY'],
            algorithm='HS256'
        )


class NormalClient(Client):
    pass
class UnauthorizedClient(Client):
    pass