import pytest

from tests.data import users
from tests.data import fines
from tests.data import teams


@pytest.fixture(scope="function")
def conf_one_player_one_team_many_fines(db_session: object) -> dict:
    """
    Creates test user
    """
    team = teams.data_one_team()
    db_session.add(team)
    db_session.commit()
    user = users.data_player(team_uuid=team.uuid)
    db_session.add(user)
    db_session.commit()
    _fines = fines.data_many_fines_per_team(team_uuid=team.uuid, n=10)
    for fine in _fines:
        db_session.add(fine)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def conf_one_banker_one_team_many_fines(db_session: object) -> dict:
    """
    Creates test user
    """
    team = teams.data_one_team()
    db_session.add(team)
    db_session.commit()
    user = users.test_admin(team_uuid=team.uuid)
    db_session.add(user)
    db_session.commit()
    _fines = fines.data_many_fines_per_team(team_uuid=team.uuid, n=10)
    for fine in _fines:
        db_session.add(fine)
    db_session.commit()
    return user
