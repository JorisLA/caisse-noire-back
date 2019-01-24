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
        player_info = {
            'first_name':'player first name 1',
            'last_name':'player last name 1',
            'email':'player1@gmail.com',
            'pw_hash':bcrypt.generate_password_hash('thisismypassword1'),
            'team_uuid':self.team_uuid,
            'banker':False
        }
        PlayerModelRepository.create_player(self, player_info=player_info)


