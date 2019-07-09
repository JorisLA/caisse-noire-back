import pytest
import uuid

from tests.conftest import db_session
from tests.data import users, teams
from caisse_noire.models.team import Team


@pytest.fixture(scope="function")
def account_signup_banker(db_session):
    return {
        'first_name': 'dummy_first_name',
        'last_name': 'dummy_last_name',
        'email': 'dummy_email',
        'password': 'dummy_password',
        'add_team': 'sdv',
    }


@pytest.fixture(scope="function")
def account_signup_player(db_session):
    team = teams.test_team()
    db_session.add(team)
    db_session.commit()
    return {
        'first_name': 'dummy_first_name',
        'last_name': 'dummy_last_name',
        'email': 'dummy_email',
        'password': 'dummy_password',
        'get_team': team.uuid,
    }


@pytest.fixture(scope="function")
def account_signup_banker_password_too_short(db_session):
    return {
        'first_name': 'dummy_first_name',
        'last_name': 'dummy_last_name',
        'email': 'dummy_email',
        'password': '1234567',
        'add_team': 'sdv',
    }


@pytest.fixture(scope="function")
def account_signup_banker_missing_parameter(db_session):
    return {
        'first_name': 'dummy_first_name',
        'last_name': '',
        'email': 'dummy_email',
        'password': '12345678',
        'add_team': 'sdv',
    }


@pytest.fixture(scope="function")
def account_signup_banker_missing_parameter_team(db_session):
    return {
        'first_name': 'dummy_first_name',
        'last_name': 'dummy_last_name',
        'email': 'dummy_email',
        'password': '12345678',
    }


@pytest.fixture(scope="function")
def account_signup_banker_empty_add_team(db_session):
    return {
        'first_name': 'dummy_first_name',
        'last_name': '',
        'email': 'dummy_email',
        'password': '12345678',
        'add_team': '',
    }


@pytest.fixture(scope="function")
def account_signup_banker_invalid_get_team(db_session):
    return {
        'first_name': 'dummy_first_name',
        'last_name': 'dummy_last_name',
        'email': 'dummy_email',
        'password': '12345678',
        'get_team': 'dummy_team',
    }


@pytest.fixture(scope="function")
def account_signup_player_team_not_found(db_session):
    return {
        'first_name': 'dummy_first_name',
        'last_name': 'dummy_last_name',
        'email': 'dummy_email',
        'password': 'dummy_password',
        'get_team': str(uuid.uuid4()),
    }


@pytest.fixture(scope="function")
def account_signin_admin(db_session):
    user = users.test_admin()
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def account_signin_player(db_session):
    user = users.test_player()
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def account_signin_player_not_found(db_session):
    return {
        'email': 'dummy_email',
        'password': 'dummy_password',
    }


@pytest.fixture(scope="function")
def account_signin_player_missing_parameter(db_session):
    return {
        'email': '',
        'password': 'dummy_password',
    }
