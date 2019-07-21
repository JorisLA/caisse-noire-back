import uuid
import database
from faker import Faker

from caisse_noire.models.player import Player, PlayerFines
from caisse_noire.models.team import Team
from caisse_noire.models.fine import Fine
from caisse_noire.common.password import Passwords
from tests.data.conf import TEST_PASSWORD
from tests.data.fines import test_fine
from tests.data.teams import test_team


def test_admin():
    team_uuid = str(uuid.uuid4())
    team = Team(uuid=team_uuid, label='sdv')
    database.db.session.add(team)
    player = Player(
        uuid=str(uuid.uuid4()),
        first_name='Example',
        last_name='Banker',
        email='Banker@somedomain.com',
        password=Passwords.hash_password(TEST_PASSWORD),
        banker=True,
        team_uuid=team_uuid,
    )
    return player


def test_player():
    team_uuid = str(uuid.uuid4())
    team = Team(uuid=team_uuid, label='sdv')
    database.db.session.add(team)
    player = Player(
        uuid=str(uuid.uuid4()),
        first_name='Example',
        last_name='Player',
        email='Player@somedomain.com',
        password=Passwords.hash_password(TEST_PASSWORD),
        banker=False,
        team_uuid=team_uuid,
    )
    return player


def test_players_from_single_team(n=10):
    fake = Faker(locale="fr_FR")
    fake.seed(42)

    team = test_team()
    database.db.session.add(team)
    database.db.session.commit()

    fine = test_fine(team_uuid=team.uuid)
    database.db.session.add(fine)
    database.db.session.commit()

    association = PlayerFines(player_fines_id=str(uuid.uuid4()))
    association.fine = fine

    players = []
    for i in range(n):
        player = Player(
            uuid=str(uuid.uuid4()),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password=Passwords.hash_password(fake.password()),
            banker=False,
            team_uuid=team.uuid,
        )
        player.fines.append(association)
        players.append(player)

    return players
