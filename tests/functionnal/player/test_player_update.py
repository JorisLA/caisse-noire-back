import uuid

from tests.functionnal import auth_for, auth_for_invalid_token


def test_update_player(client, banker, player):
    response = client.put(
        f"/players/{player['user'].uuid}",
        headers={
            'x-access-token': auth_for(banker)
        },
        json={
            'fine_uuid': player['fine'].uuid
        }
    )
    player_total = response.get_json()['total']

    assert isinstance(player_total, int)
    assert player_total == player['fine'].cost
    assert response.status_code == 200


def test_update_player_invalid_token(client, banker, player):
    response = client.put(
        f"/players/{player['user'].uuid}",
        headers={
            'x-access-token': auth_for_invalid_token(banker)
        },
        json={
            'fine_uuid': player['fine'].uuid
        }
    )

    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_invalid'


def test_update_player_missing_token(client, banker, player):
    response = client.put(
        f"/players/{player['user'].uuid}",
        json={
            'fine_uuid': player['fine'].uuid
        }
    )

    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_missing'


def test_update_player_unauthorized(client, player):
    response = client.put(
        f"/players/{player['user'].uuid}",
        headers={
            'x-access-token': auth_for(player['user'])
        },
        json={
            'fine_uuid': player['fine'].uuid
        }
    )

    assert response.status_code == 403
    assert response.get_json()['message'] == 'player_unauthorized'


def test_update_unknown_player(client, banker, player):
    response = client.put(
        f"/players/{uuid.uuid4()}",
        headers={
            'x-access-token': auth_for(banker)
        },
        json={
            'fine_uuid': player['fine'].uuid
        }
    )

    assert response.status_code == 404
    assert response.get_json()['message'] == 'player_not_found'


def test_update_missing_parameter(client, banker, player):
    response = client.put(
        f"/players/{player['user'].uuid}",
        headers={
            'x-access-token': auth_for(banker)
        },
    )

    assert response.status_code == 422
    assert response.get_json()['message'] == 'missing_parameter'


def test_update_unknown_fine(client, banker, player):
    response = client.put(
        f"/players/{player['user'].uuid}",
        headers={
            'x-access-token': auth_for(banker)
        },
        json={
            'fine_uuid': uuid.uuid4()
        }
    )

    assert response.get_json()['message'] == 'fine_not_found'
    assert response.status_code == 404
