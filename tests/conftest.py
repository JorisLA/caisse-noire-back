"""
Create ressources for tests
"""
import uuid
import pytest

from app import (
    bcrypt,
    create_app
)
import database
from caisse_noire.models.player import Player
from caisse_noire.models.team import Team
from caisse_noire.models.fine import Fine
from caisse_noire.models.repository.player_repository import PlayerFines

from tests import setup_db, teardown_db, clean_db
from tests.data import users, teams


@pytest.fixture(scope="session")
def app():
    """Global skylines application fixture

    Initialized with testing config file.
    """
    yield create_app()


@pytest.fixture(scope="session")
def db(app):
    """Creates clean database schema and drops it on teardown

    Note, that this is a session scoped fixture, it will be executed only once
    and shared among all tests. Use `db_session` fixture to get clean database
    before each test.
    """

    setup_db(app)
    yield database.db
    teardown_db()


@pytest.fixture(scope="function")
def db_session(db, app):
    """Provides clean database before each test. After each test,
    session.rollback() is issued.

    Return sqlalchemy session.
    """

    with app.app_context():
        clean_db()
        yield db.session
        db.session.rollback()


@pytest.fixture(scope="function")
def banker(db_session):
    user = users.test_admin()
    db_session.add(user)
    db_session.commit()
    return user


# @pytest.fixture(scope='module')
# def new_player_banker():
#     pw_hash = bcrypt.generate_password_hash('thisismypassword')
#     player = Player(
#         first_name='player first name',
#         last_name='player last name',
#         email='player@gmail.com',
#         uuid=str(uuid.uuid4()),
#         team_uuid=str(uuid.uuid4()),
#         password=pw_hash,
#         banker=True,
#     )
#     return player


# @pytest.fixture(scope='module')
# def new_team():
#     team = Team(
#         uuid=str(uuid.uuid4()),
#         label='team name',
#     )
#     return team


# @pytest.fixture(scope='module')
# def new_fine():
#     fine = Fine(
#         uuid=str(uuid.uuid4()),
#         label='fine name',
#         cost=5,
#         team_uuid=str(uuid.uuid4()),
#     )
#     return fine


# @pytest.fixture(scope='module')
# def new_player_fine_association(new_fine, new_player_banker):
#     player_fines = PlayerFines()
#     player_fines.fine_uuid = new_fine.uuid
#     player_fines.player_uuid = new_player_banker.uuid
#     player_fines.player_fines_id = str(uuid.uuid4())
#     return player_fines


# @pytest.fixture(scope='module')
# def simple_client():
#     simple_client = Client()

#     yield simple_client

#     simple_client.ctx.pop()
#     # db.drop_all()
