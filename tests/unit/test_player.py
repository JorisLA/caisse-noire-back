def test_new_player(new_player):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_player.first_name == 'player first name'
    assert new_player.last_name == 'player last name'
    assert new_player.email == 'player@gmail.com'
    assert new_player.uuid
    assert new_player.team_uuid
    assert new_player.password
    assert new_player.banker == True
    assert not new_player.fines