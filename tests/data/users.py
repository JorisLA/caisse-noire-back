import uuid
import database

from caisse_noire.models.player import Player
from caisse_noire.models.team import Team
from caisse_noire.common.password import Passwords


def test_admin():
    team_uuid = str(uuid.uuid4())
    team = Team(uuid=team_uuid, label='sdv')
    database.db.session.add(team)
    # db.session.commit()
    player = Player(
        uuid=str(uuid.uuid4()),
        first_name='Example',
        last_name='Banker',
        email='Banker@somedomain.com',
        password=Passwords.hash_password('managepass'),
        banker=True,
        team_uuid=team_uuid,
    )
    return player
