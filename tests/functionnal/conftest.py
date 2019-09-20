import pytest

from app import create_app, os
from tests.data import users
from tests.data import fines
from tests.data import teams
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
from caisse_noire.api.v1.ping.ping import PingHandler


@pytest.fixture(scope="session")
def app():
    """Global skylines application fixture

    Initialized with testing config file.
    """
    app_test = create_app()
    app_test.config.from_object(os.environ['APP_SETTINGS'])
    ctx = app_test.app_context()
    ctx.push()
    return app_test


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def test_list_players(db_session: object) -> dict:
    """
    Creates 10 test users
    """
    _users = users.test_players_from_single_team()
    for player in _users:
        db_session.add(player)
    db_session.commit()
    return _users


@pytest.fixture(scope="function")
def player(db_session: object) -> dict:
    user = users.test_player()
    db_session.add(user)
    db_session.commit()
    fine = fines.test_fine(user.team_uuid)
    db_session.add(fine)
    db_session.commit()
    return {
        'user': user,
        'fine': fine,
    }


@pytest.fixture(scope="function")
def banker(db_session):
    user = users.test_admin()
    db_session.add(user)
    db_session.commit()
    return user
