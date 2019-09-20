"""
Unit test for fine model
"""


def test_new_fine(new_fine):
    """
    GIVEN a Fine model
    WHEN a new Fine is created
    THEN check its fields are defined correctly
    """
    assert new_fine.uuid
    assert new_fine.label == 'fine name'
    assert new_fine.cost == 5
    assert new_fine.team_uuid
