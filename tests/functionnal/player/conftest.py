import pytest

from tests.data import users


@pytest.fixture(scope="function")
def banker(db_session):
    user = users.test_admin()
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def test_list_players(db_session):
    """
    Creates 10 test users
    """
    _users = users.test_players_from_single_team()
    for player in _users:
        db_session.add(player)
    db_session.commit()
    return _users
