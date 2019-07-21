from tests.functionnal import auth_for


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
