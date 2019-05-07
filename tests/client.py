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
from caisse_noire.models.repository.fine_repository import FineModelRepository
from caisse_noire.models.repository.player_repository import PlayerModelRepository
from caisse_noire.models.repository.team_repository import TeamModelRepository
from caisse_noire.api.v1.players.players import PlayersHandler
from caisse_noire.api.v1.players.player import PlayerHandler
from caisse_noire.api.v1.players.fines import PlayersFinesHandler
from caisse_noire.api.v1.players.fine import PlayerFineHandler
from caisse_noire.api.v1.fines.fines import FinesHandler
from caisse_noire.api.v1.fines.fine import FineHandler
from caisse_noire.api.v1.players.signin import SigninHandler
from caisse_noire.api.v1.players.signup import SignupHandler
from caisse_noire.api.v1.statistics.statistics import StatisticsHandler
from caisse_noire.api.v1.teams.teams import TeamsHandler


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
        self.app_test.add_url_rule('/players', view_func=PlayersHandler.as_view('players'))
        self.app_test.add_url_rule('/players/<player_uuid>', view_func=PlayerHandler.as_view('player'))
        self.app_test.add_url_rule('/players/fines', view_func=PlayersFinesHandler.as_view('players_fines'))
        self.app_test.add_url_rule('/players/<player_uuid>/fine', view_func=PlayerFineHandler.as_view('player_fine'))
        self.app_test.add_url_rule('/fines', view_func=FinesHandler.as_view('fines'))
        self.app_test.add_url_rule('/fines/<fine_uuid>', view_func=FineHandler.as_view('fine'))
        self.app_test.add_url_rule('/players/signin', view_func=SigninHandler.as_view('player_signin'))
        self.app_test.add_url_rule('/players/signup', view_func=SignupHandler.as_view('player_signup'))
        self.app_test.add_url_rule('/statistics', view_func=StatisticsHandler.as_view('statistics'))
        self.app_test.add_url_rule('/teams', view_func=TeamsHandler.as_view('teams'))
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