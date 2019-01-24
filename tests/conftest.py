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
from views.players.views import PlayerApi
from views.fines.views import FineApi
from views.players_fines.views import BillApi
from views.signin.views import SigninApi
from views.signup.views import SignupApi
from views.teams.views import TeamApi
from views.statistics.views import StatisticApi
from tests.db import PopulateDatabaseAsAdmin
 
class HttpClient(PopulateDatabaseAsAdmin):
    pass

@pytest.fixture(scope='module')
def new_player():
    pw_hash = bcrypt.generate_password_hash('thisismypassword')
    user_uuid=str(uuid.uuid4())
    team_uuid=str(uuid.uuid4())
    player = Player(
        first_name='player first name',
        last_name='player last name',
        email='player@gmail.com',
        uuid=user_uuid,
        team_uuid=team_uuid,
        password=pw_hash,
        banker=True,
    )
    return player


@pytest.fixture(scope='module')
def banker():
    client = HttpClient()
    client.bankerClient()
    client.add_players_from_team()

    yield client  # this is where the testing happens!
 
    client.ctx.pop()
    db.drop_all()

