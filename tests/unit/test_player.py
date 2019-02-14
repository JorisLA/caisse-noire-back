def test_new_player(new_player_banker):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check its fields are defined correctly
    """
    assert new_player_banker.first_name == 'player first name'
    assert new_player_banker.last_name == 'player last name'
    assert new_player_banker.email == 'player@gmail.com'
    assert new_player_banker.uuid
    assert new_player_banker.team_uuid
    assert new_player_banker.password
    assert new_player_banker.banker == True
    assert not new_player_banker.fines

def test_new_player_fine_association(new_player_fine_association):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check its fields are defined correctly
    """
    assert new_player_fine_association.fine_uuid
    assert new_player_fine_association.player_uuid
    assert new_player_fine_association.player_fines_id