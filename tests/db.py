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
from caisse_noire.models.repository.fine_repository import FineModelRepository
from caisse_noire.models.repository.player_repository import PlayerModelRepository
from caisse_noire.models.repository.team_repository import TeamModelRepository
from caisse_noire.models.fine import Fine
from caisse_noire.models.player import PlayerFines
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

