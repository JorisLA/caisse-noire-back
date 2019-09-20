def test_account_banker_signup(client, account_signup_banker):
    response = client.post(
        '/players/signup',
        json=account_signup_banker
    )
    assert response.status_code == 204


def test_account_player_signup(client, account_signup_player):
    response = client.post(
        '/players/signup',
        json=account_signup_player
    )
    assert response.status_code == 204


def test_account_banker_signup_missing_parameter(
    client,
    account_signup_banker_missing_parameter
):
    response = client.post(
        '/players/signup',
        json=account_signup_banker_missing_parameter
    )
    assert response.status_code == 422
    assert response.get_json()['message'] == 'missing_parameter'


def test_account_signup_banker_password_too_short(
    client,
    account_signup_banker_password_too_short
):
    response = client.post(
        '/players/signup',
        json=account_signup_banker_password_too_short
    )
    assert response.status_code == 422
    assert response.get_json()['message'] == 'invalid_password'


def test_account_signup_banker_empty_add_team(
    client,
    account_signup_banker_empty_add_team
):
    response = client.post(
        '/players/signup',
        json=account_signup_banker_empty_add_team
    )
    assert response.status_code == 422
    assert response.get_json()['message'] == 'missing_parameter'


def test_account_signup_banker_missing_parameter_team(
    client,
    account_signup_banker_missing_parameter_team
):
    response = client.post(
        '/players/signup',
        json=account_signup_banker_missing_parameter_team
    )
    assert response.status_code == 422
    assert response.get_json()['message'] == 'missing_parameter'


def test_account_signup_banker_invalid_parameter_team(
    client,
    account_signup_banker_invalid_get_team
):
    response = client.post(
        '/players/signup',
        json=account_signup_banker_invalid_get_team
    )
    assert response.status_code == 422
    assert response.get_json()['message'] == 'invalid_parameter'


def test_account_signup_banker_team_not_found(
    client,
    account_signup_player_team_not_found
):
    response = client.post(
        '/players/signup',
        json=account_signup_player_team_not_found
    )
    assert response.status_code == 404
    assert response.get_json()['message'] == 'team_not_found'
