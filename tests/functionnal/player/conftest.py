import pytest

from tests.data import users
from tests.data import fines


@pytest.fixture(scope="function")
def test_player_with_fines(db_session: object) -> dict:
    """
    Creates 10 test users
    """
    _users = users.test_players_from_single_team(n=1)
    for player in _users:
        db_session.add(player)
    db_session.commit()
    return _users
