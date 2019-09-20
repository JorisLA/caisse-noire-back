import uuid
from faker import Faker

from caisse_noire.models.fine import Fine


def test_fine(team_uuid: uuid) -> object:
    fine = Fine(
        uuid=str(uuid.uuid4()),
        cost=2,
        label='oubli',
        team_uuid=team_uuid
    )
    return fine


def test_fines(team_uuid: uuid, n: int) -> object:
    fake = Faker(locale="fr_FR")
    fake.seed(42)
    fines = []
    for i in range(n):
        fine = Fine(
            uuid=str(uuid.uuid4()),
            cost=2,
            label=fake.first_name(),
            team_uuid=team_uuid
        )
        fines.append(fine)

    return fines


def data_many_fines_per_team(team_uuid: uuid, n: int) -> Fine:
    fake = Faker(locale="fr_FR")
    fake.seed(42)
    fines = []
    for i in range(n):
        fine = Fine(
            uuid=str(uuid.uuid4()),
            cost=2,
            label=fake.first_name(),
            team_uuid=team_uuid
        )
        fines.append(fine)

    return fines
