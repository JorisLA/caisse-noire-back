def test_account_creation(simple_client):
    """
    """

    response = simple_client.test_client.post('/signup',
        json={
            'first_name':'dummy_first_name',
            'last_name':'dummy_last_name',
            'email':'dummy_email',
            'password':'dummy_password',
            'banker':True,
            'add_team':'sdv2',
        }
    )
    print(response.get_json())
    #assert response.status_code == 200
