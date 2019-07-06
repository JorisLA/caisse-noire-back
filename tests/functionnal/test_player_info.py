from tests.functionnal import auth_for


def test_get_player_fines_empty(client, banker):
    response = client.get(
        '/players/{}/fine'.format(banker.uuid),
        headers={
            'x-access-token': auth_for(banker)
        }
    )
    value = response.get_json()['fines']
    assert isinstance(value, dict)
    assert not value
    assert response.status_code == 200
