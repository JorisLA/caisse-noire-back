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
# def new_fine():
#     fine = Fine(
#         uuid=str(uuid.uuid4()),
#         label='fine name',
#         cost=5,
#         team_uuid=str(uuid.uuid4()),
#     )
#     return fine
