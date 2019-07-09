from tests.functionnal import auth_for


def test_get_player_list(client, test_list_players):
    response = client.get(
        '/players'.format(test_list_players[0].uuid),
        headers={
            'x-access-token': auth_for(test_list_players[0])
        }
    )
    players_list = response.get_json()['players']
    fines_list = response.get_json()['fines']
    print(response.get_json())
    assert isinstance(players_list, list)
    assert isinstance(fines_list, list)
    assert response.status_code == 200
