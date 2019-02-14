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
from tests.client import Client, AdminClient
from models.repository.fine_repository import FineModelRepository
from models.repository.player_repository import PlayerModelRepository
from models.repository.team_repository import TeamModelRepository
from models.fine import Fine
from models.player import PlayerFines
from views.players.views import PlayerApi
from views.fines.views import FineApi
from views.players_fines.views import BillApi
from views.signin.views import SigninApi
from views.signup.views import SignupApi
from views.teams.views import TeamApi
from views.statistics.views import StatisticApi

class PopulateDatabaseAsAdmin(AdminClient):
    """
    Populate database class
    """
    def add_players_from_team(self):
        fine = Fine(
            uuid=str(uuid.uuid4()),
            label='fine name',
            cost=5,
        )
        db.session.add(fine)
        db.session.commit()
        for x in range(5):
            player_info = {
                'first_name':'player first name {}'.format(x),
                'last_name':'player last name {}'.format(x),
                'email':'player{}@gmail.com'.format(x),
                'pw_hash':bcrypt.generate_password_hash('thisismypassword1'),
                'team_uuid':self.team_uuid,
                'banker':False
            }
            player_uuid = PlayerModelRepository.create_player(self, player_info=player_info)
            player_fines = PlayerFines()
            player_fines.fine_uuid = fine.uuid
            player_fines.player_uuid = player_uuid
            player_fines.player_fines_id = str(uuid.uuid4())
            db.session.add(player_fines)
            db.session.commit()

