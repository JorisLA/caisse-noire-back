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
    Team,
    Fine,
    PlayerFines,
)
from views.players.views import PlayerApi
from views.fines.views import FineApi
from views.players_fines.views import BillApi
from views.signin.views import SigninApi
from views.signup.views import SignupApi
from views.teams.views import TeamApi
from views.statistics.views import StatisticApi
from tests.db import PopulateDatabaseAsAdmin
from tests.client import Client
 
class HttpClient(PopulateDatabaseAsAdmin):
    pass

@pytest.fixture(scope='module')
def new_player_banker():
    pw_hash = bcrypt.generate_password_hash('thisismypassword')
    player = Player(
        first_name='player first name',
        last_name='player last name',
        email='player@gmail.com',
        uuid=str(uuid.uuid4()),
        team_uuid=str(uuid.uuid4()),
        password=pw_hash,
        banker=True,
    )
    return player

@pytest.fixture(scope='module')
def new_team():
    team = Team(
        uuid=str(uuid.uuid4()),
        label='team name',
    )
    return team

@pytest.fixture(scope='module')
def new_fine():
    fine = Fine(
        uuid=str(uuid.uuid4()),
        label='fine name',
        cost=5,
    )
    return fine

@pytest.fixture(scope='module')
def new_player_fine_association(new_fine, new_player_banker):
    player_fines = PlayerFines()
    player_fines.fine_uuid = new_fine.uuid
    player_fines.player_uuid = new_player_banker.uuid
    player_fines.player_fines_id = str(uuid.uuid4())
    return player_fines

@pytest.fixture(scope='module')
def banker():
    client = HttpClient()
    client.bankerClient()
    client.add_players_from_team()

    yield client  # this is where the testing happens!
 
    client.ctx.pop()
    #db.drop_all()

@pytest.fixture(scope='module')
def simple_client():
    simple_client = Client()

    yield simple_client

    simple_client.ctx.pop()
    db.drop_all()
