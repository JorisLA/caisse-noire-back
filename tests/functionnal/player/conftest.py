import pytest

from tests.data import users
from tests.data import fines


@pytest.fixture(scope="function")
def banker(db_session: object) -> dict:
    user = users.test_admin()
    db_session.add(user)
    db_session.commit()
    return user


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
def test_player_with_fines(db_session: object) -> dict:
    """
    Creates 10 test users
    """
    _users = users.test_players_from_single_team(n=1)
    for player in _users:
        db_session.add(player)
    db_session.commit()
    return _users
