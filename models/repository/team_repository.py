import uuid

from app import db, text, func
from models.team import Team, TeamFines

class TeamModelRepository(object):
    """
    """

    def get_team_by_uuid(
        self,
        team_uuid,
    ):
        return Team.query.filter_by(uuid=team_uuid).first()

    def get_teams(
        self,
    ):
        final_result = []
        teams = Team.query.all()
        for team in teams:
            final_result.append({
                'value': team.uuid,
                'text': team.label,
            })
        return final_result

    def create_team(
        self,
        team_name,
    ):
        team_uuid = str(uuid.uuid4())
        team = Team(uuid=team_uuid, label=team_name)
        db.session.add(team)
        return team_uuid
