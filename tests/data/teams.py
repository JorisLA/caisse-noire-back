import uuid

from caisse_noire.models.team import Team


def test_team():
    team_uuid = str(uuid.uuid4())
    team = Team(uuid=team_uuid, label='sdv')
    return team


def data_one_team() -> Team:
    team_uuid = str(uuid.uuid4())
    team = Team(uuid=team_uuid, label='sdv')
    return team
