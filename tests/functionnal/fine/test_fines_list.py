from tests.functionnal import auth_for, auth_for_invalid_token
from caisse_noire.common.settings import MAX_PER_PAGE


def test_get_fines_list_first_page(
    client,
    conf_one_player_one_team_many_fines
):
    response = client.get(
        '/fines',
        headers={
            'x-access-token': auth_for(conf_one_player_one_team_many_fines)
        }
    )
    fines_list = response.get_json()['fines']

    assert isinstance(fines_list, list)
    assert len(fines_list) <= MAX_PER_PAGE
    assert response.status_code == 200


def test_get_fines_list_per_page(client, conf_one_player_one_team_many_fines):
    _perPage = 10
    response = client.get(
        f'/fines?_perPage={_perPage}',
        headers={
            'x-access-token': auth_for(conf_one_player_one_team_many_fines)
        }
    )
    fines_list = response.get_json()['fines']

    assert isinstance(fines_list, list)
    assert len(fines_list) == _perPage
    assert response.status_code == 200


def test_get_fines_list_second_page(
    client,
    conf_one_player_one_team_many_fines
):
    first_page = client.get(
        '/fines',
        headers={
            'x-access-token': auth_for(conf_one_player_one_team_many_fines)
        }
    )
    _lastUuid = first_page.get_json()['fines'][-1]['uuid']
    second_page = client.get(
        f'/fines?_currentPage=2&_lastUuid={_lastUuid}',
        headers={
            'x-access-token': auth_for(conf_one_player_one_team_many_fines)
        }
    )
    fines_list = second_page.get_json()['fines']

    assert isinstance(fines_list, list)
    assert len(fines_list) <= MAX_PER_PAGE
    assert second_page.status_code == 200


def test_get_fines_list_filter_by_label(
    client,
    conf_one_player_one_team_many_fines
):
    first_page = client.get(
        '/fines',
        headers={
            'x-access-token': auth_for(conf_one_player_one_team_many_fines)
        }
    )
    label = first_page.get_json()['fines'][-1]['label']
    response = client.get(
        f'/fines?_filter={label}',
        headers={
            'x-access-token': auth_for(conf_one_player_one_team_many_fines)
        }
    )
    fine = response.get_json()['fines']

    assert isinstance(fine, list)
    assert len(fine) == 1
    assert fine[0]['label'] == label
    assert response.status_code == 200


def test_update_fine_invalid_token(
    client,
    conf_one_banker_one_team_many_fines,
):
    response = client.get(
        '/fines',
        headers={
            'x-access-token': auth_for_invalid_token(
                conf_one_banker_one_team_many_fines
            ),
        }
    )
    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_invalid'


def test_update_fine_missing_token(
    client,
    conf_one_banker_one_team_many_fines,
):
    response = client.get(
        '/fines',
    )

    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_missing'
