import uuid

from tests.functionnal import auth_for, auth_for_invalid_token


def test_get_player_list_first_page(client, test_list_players):
    response = client.get(
        '/players',
        headers={
            'x-access-token': auth_for(test_list_players[0])
        }
    )
    players_list = response.get_json()['players']

    assert isinstance(players_list, list)
    assert test_list_players[9].first_name not in players_list
    assert response.get_json()['full_count'] == len(test_list_players)
    assert response.status_code == 200


def test_get_player_list_first_page_invalid_token(client, test_list_players):
    response = client.get(
        '/players',
        headers={
            'x-access-token': auth_for_invalid_token(test_list_players[0])
        }
    )

    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_invalid'


def test_get_player_list_first_page_missing_token(client, test_list_players):
    response = client.get(
        '/players',
    )

    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_missing'


def test_get_player_list_second_page(client, test_list_players):
    response = client.get(
        f'/players?_lastUuid={test_list_players[5].uuid}',
        headers={
            'x-access-token': auth_for(test_list_players[0])
        }
    )
    players_list = response.get_json()['players']

    assert isinstance(players_list, list)
    assert test_list_players[0].first_name not in players_list
    assert response.get_json()['full_count'] == len(test_list_players)
    assert response.status_code == 200


def test_get_player_list_filter_by_first_name(
    client,
    test_list_players
):
    response = client.get(
        f'/players?_filter={test_list_players[0].first_name}',
        headers={
            'x-access-token': auth_for(test_list_players[0])
        }
    )

    players_list = response.get_json()['players']

    assert isinstance(players_list, list)
    assert players_list[0]['first_name'] == test_list_players[0].first_name
    assert response.get_json()['full_count'] == len(test_list_players)
    assert response.status_code == 200


def test_get_player_list_filter_by_last_name(
    client,
    test_list_players
):
    response = client.get(
        f'/players?_filter={test_list_players[0].last_name}',
        headers={
            'x-access-token': auth_for(test_list_players[0])
        }
    )

    players_list = response.get_json()['players']

    assert isinstance(players_list, list)
    assert players_list[0]['last_name'] == test_list_players[0].last_name
    assert response.get_json()['full_count'] == len(test_list_players)
    assert response.status_code == 200


def test_get_player_list_filter_by_unknown_name(
    client,
    test_list_players
):
    response = client.get(
        f'/players?_filter=JohnyJohn',
        headers={
            'x-access-token': auth_for(test_list_players[0])
        }
    )

    players_list = response.get_json()['players']

    assert isinstance(players_list, list)
    assert not players_list
    assert response.get_json()['full_count'] == len(test_list_players)
    assert response.status_code == 200


def test_get_player_list_by_unknown_uuid(client, test_list_players):
    response = client.get(
        f'/players?_lastUuid={str(uuid.uuid4())}',
        headers={
            'x-access-token': auth_for(test_list_players[0])
        }
    )

    assert response.status_code == 404
    assert response.get_json()['message'] == 'player_not_found'
