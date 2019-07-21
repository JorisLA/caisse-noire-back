import uuid

from caisse_noire.models.fine import Fine


def test_fine(team_uuid: uuid) -> object:
    fine = Fine(
        uuid=str(uuid.uuid4()),
        cost=2,
        label='oubli',
        team_uuid=team_uuid
    )
    return fine
