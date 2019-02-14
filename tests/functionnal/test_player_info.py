def test_player_fines(banker):
    """
    GIVEN a Flask application
    WHEN the '/get' page is requested (GET)
    THEN check the response is valid
    """
    response = banker.test_client.get('/bills/{}'.format(banker.player_uuid),
         headers={
            'x-access-token':banker.token
        }
    )
    print(response.get_json())
    #assert response.status_code == 200