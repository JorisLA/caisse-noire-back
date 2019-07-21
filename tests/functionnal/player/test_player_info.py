import uuid

from tests.functionnal import auth_for


def test_get_player_empty_history(client, banker):
    response = client.get(
        f'/players/{banker.uuid}/fine',
        headers={
            'x-access-token': auth_for(banker)
        }
    )

    value = response.get_json()['fines']
    assert isinstance(value, dict)
    assert not value
    assert response.status_code == 200


def test_get_player_history(client, banker, test_player_with_fines):
    response = client.get(
        f"/players/{test_player_with_fines[0].uuid}/fine",
        headers={
            'x-access-token': auth_for(banker)
        }
    )

    player_history = response.get_json()['fines']

    assert isinstance(player_history, dict)
    for player in test_player_with_fines[0].fines:
        assert player.fine.label in player_history.keys()
    assert response.status_code == 200


def test_get_player_history_unknown_player(client, banker):
    response = client.get(
        f"/players/{uuid.uuid4()}/fine",
        headers={
            'x-access-token': auth_for(banker)
        }
    )

    assert response.status_code == 404
    assert response.get_json()['message'] == 'player_not_found'


def test_delete_player_history(client, banker, test_player_with_fines):
    response = client.delete(
        f"/players/{test_player_with_fines[0].uuid}/fine",
        headers={
            'x-access-token': auth_for(banker)
        }
    )

    assert response.status_code == 204


def test_delete_player_history_unauthorized(
    client,
    test_player_with_fines
):
    response = client.delete(
        f"/players/{test_player_with_fines[0].uuid}/fine",
        headers={
            'x-access-token': auth_for(test_player_with_fines[0])
        }
    )

    assert response.status_code == 403
    assert response.get_json()['message'] == 'player_unauthorized'


def test_delete_player_history_unknown_player(
    client,
    banker,
    test_player_with_fines
):
    response = client.delete(
        f"/players/{uuid.uuid4()}/fine",
        headers={
            'x-access-token': auth_for(banker)
        }
    )

    assert response.status_code == 404
    assert response.get_json()['message'] == 'player_not_found'
