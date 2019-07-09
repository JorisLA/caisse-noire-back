from tests.data.conf import TEST_PASSWORD


def test_account_signin_admin(
    client,
    account_signin_admin
):
    response = client.post(
        '/players/signin',
        json={
            'email': account_signin_admin.email,
            'password': TEST_PASSWORD,
        }
    )
    assert response.status_code == 200
    assert response.get_json()['banker'] is True
    assert response.get_json()['token']


def test_account_signin_player(
    client,
    account_signin_player
):
    response = client.post(
        '/players/signin',
        json={
            'email': account_signin_player.email,
            'password': TEST_PASSWORD,
        }
    )
    assert response.status_code == 200
    assert response.get_json()['banker'] is False
    assert response.get_json()['token']


def test_account_signin_player_not_found(
    client,
    account_signin_player_not_found
):
    response = client.post(
        '/players/signin',
        json=account_signin_player_not_found
    )
    assert response.status_code == 404
    assert response.get_json()['message'] == 'player_not_found'


def test_account_signin_player_missing_parameter(
    client,
    account_signin_player_missing_parameter
):
    response = client.post(
        '/players/signin',
        json=account_signin_player_missing_parameter
    )
    assert response.status_code == 422
    assert response.get_json()['message'] == 'missing_parameter'
