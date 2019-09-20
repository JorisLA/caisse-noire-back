from tests.functionnal import auth_for, auth_for_invalid_token


def test_create_fine(client, banker):
    response = client.post(
        f'/fines',
        headers={
            'x-access-token': auth_for(banker)
        },
        json={
            'cost': 2,
            'label': 'dummy_fine',
        }
    )

    assert response.status_code == 201
    assert response.get_json()['message'] == 'Fine added!'
    assert response.get_json()['status'] == 'success'


def test_create_fine_unauthorized(client, player):
    response = client.post(
        f'/fines',
        headers={
            'x-access-token': auth_for(player['user'])
        },
        json={
            'cost': 2,
            'label': 'dummy_fine',
        }
    )

    assert response.status_code == 403
    assert response.get_json()['message'] == 'player_unauthorized'


def test_create_fine_missing_parameters(client, banker):
    response = client.post(
        f'/fines',
        headers={
            'x-access-token': auth_for(banker)
        },
        json={
            'cost': 2,
        }
    )

    assert response.status_code == 422
    assert response.get_json()['message'] == 'missing_parameter'


def test_create_fine_invalid_token(
    client,
    banker,
):
    response = client.post(
        '/fines',
        headers={
            'x-access-token': auth_for_invalid_token(banker),
        },
        json={
            'cost': 2,
            'label': 'dummy_fine',
        }
    )

    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_invalid'


def test_update_fine_missing_token(
    client,
    banker,
):
    response = client.post(
        f'/fines',
        json={
            'cost': 2,
            'label': 'dummy_fine',
        }
    )

    assert response.status_code == 401
    assert response.get_json()['message'] == 'token_missing'
