import uuid
import database
from faker import Faker

from caisse_noire.models.player import Player, PlayerFines
from caisse_noire.models.team import Team
from caisse_noire.models.fine import Fine
from caisse_noire.common.password import Passwords
from tests.data.conf import TEST_PASSWORD


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


def test_players_from_single_team(n=2):
    fake = Faker(locale="fr_FR")
    fake.seed(42)

    team_uuid = str(uuid.uuid4())
    team = Team(uuid=team_uuid, label='sdv')
    database.db.session.add(team)
    database.db.session.commit()

    fine_uuid = str(uuid.uuid4())
    fine = Fine(
        uuid=fine_uuid,
        cost=2,
        label='oubli',
        team_uuid=team_uuid
    )
    database.db.session.add(fine)

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
            team_uuid=team_uuid,
        )
        player.fines.append(association)
        players.append(player)

    return players
