"""
Unit test for team model
"""
def test_new_team(new_team):
    """
    GIVEN a Team model
    WHEN a new Team is created
    THEN check its fields are defined correctly
    """
    assert new_team.uuid
    assert new_team.label == 'team name'
