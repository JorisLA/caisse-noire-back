import uuid

from tests.functionnal import auth_for, auth_for_invalid_token
from caisse_noire.common.settings import MAX_PER_PAGE


def test_delete_fine(
    client,
    conf_one_banker_one_team_many_fines
):
    first_page = client.get(
        '/fines',
        headers={
            'x-access-token': auth_for(conf_one_banker_one_team_many_fines),
        }
    )
    fine_uuid = first_page.get_json()['fines'][-1]['uuid']

    response = client.delete(
        f'/fines/{fine_uuid}',
        headers={
            'x-access-token': auth_for(conf_one_banker_one_team_many_fines),
        },
    )

    assert response.status_code == 204


def test_delete_fine_unauthorized(
    client,
    conf_one_player_one_team_many_fines
):
    first_page = client.get(
        '/fines',
        headers={
            'x-access-token': auth_for(conf_one_player_one_team_many_fines),
        }
    )
    fine_uuid = first_page.get_json()['fines'][-1]['uuid']

    response = client.delete(
        f'/fines/{fine_uuid}',
        headers={
            'x-access-token': auth_for(conf_one_player_one_team_many_fines),
        },
    )

    assert response.status_code == 403
    assert response.get_json()['message'] == 'player_unauthorized'


def test_delete_unknown_fine(
    client,
    conf_one_banker_one_team_many_fines
):
    first_page = client.get(
        '/fines',
        headers={
            'x-access-token': auth_for(conf_one_banker_one_team_many_fines),
        }
    )
    fine_uuid = str(uuid.uuid4())

    response = client.delete(
        f'/fines/{fine_uuid}',
        headers={
            'x-access-token': auth_for(conf_one_banker_one_team_many_fines),
        },
    )

    assert response.status_code == 404
    assert response.get_json()['message'] == 'fine_not_found'


def test_delete_fine_invalid_token(
    client,
    conf_one_banker_one_team_many_fines,
):
    first_page = client.get(
        '/fines',
        headers={
            'x-access-token': auth_for(conf_one_banker_one_team_many_fines),
        }
    )
    fine_uuid = str(uuid.uuid4())

    response = client.delete(
        f'/fines/{fine_uuid}',
        headers={
            'x-access-token': auth_for_invalid_token(
                conf_one_banker_one_team_many_fines
            )
        },
    )

    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_invalid'


def test_delete_fine_missing_token(
    client,
    conf_one_banker_one_team_many_fines,
):
    first_page = client.get(
        '/fines',
        headers={
            'x-access-token': auth_for(conf_one_banker_one_team_many_fines),
        }
    )
    fine_uuid = str(uuid.uuid4())

    response = client.delete(
        f'/fines/{fine_uuid}',
    )

    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_missing'
