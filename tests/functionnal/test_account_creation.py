def test_account_banker_creation(client, account_creation):
    response = client.post(
        '/players/signup',
        json={
            'first_name': 'dummy_first_name',
            'last_name': 'dummy_last_name',
            'email': 'dummy_email',
            'password': 'dummy_password',
            'add_team': 'sdv',
        }
    )
    assert response.status_code == 204


def test_account_player_creation(client, account_creation_player):
    response = client.post(
        '/players/signup',
        json={
            'first_name': 'dummy_first_name',
            'last_name': 'dummy_last_name',
            'email': 'dummy_email',
            'password': 'dummy_password',
            'get_team': account_creation_player.uuid,
        }
    )
    assert response.status_code == 204
