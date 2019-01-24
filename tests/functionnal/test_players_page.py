def test_players_page(banker):
    """
    GIVEN a Flask application
    WHEN the '/get' page is requested (GET)
    THEN check the response is valid
    """
    response = banker.test_client.get('/players',
         headers={
            'x-access-token':banker.token
        }
    )

    assert response.status_code == 200
    assert response.is_json
    assert isinstance(response.get_json()['fines'], list)
    assert isinstance(response.get_json()['players'], list)
    assert isinstance(response.get_json()['full_count'], int)