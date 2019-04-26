import uuid

from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

from models.team import Team
from models.fine import Fine
from models.player import Player, PlayerFines
from flask import current_app
db = SQLAlchemy(current_app)

class TeamModelRepository(object):
    """
    """

    def get_team_by_uuid(
        self,
        team_uuid,
    ):
        return db.session.query(Team).filter_by(uuid=team_uuid).first()

    def get_teams(
        self,
    ):
        final_result = []
        teams = db.session.query(Team).all()
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

    def get_best_contributor(
        self,
        team_uuid,
    ):
        result = db.session.query(
                func.sum(Fine.cost),
                Player.first_name,
                Player.last_name,
                Player.uuid
            ).join(
                PlayerFines, (Fine.uuid==PlayerFines.fine_uuid)
            ).join(
                Player, (PlayerFines.player_uuid==Player.uuid)
            ).filter(
                Fine.team_uuid==team_uuid,
            ).group_by(
                Player.uuid
            ).order_by(
                func.sum(Fine.cost).desc()
            ).first()
        if result:
            return {
                'total': result[0],
                'first_name': result[1],
                'last_name': result[2],
            }
        else:
            return {}

    def get_most_recurrent_fine(
        self,
        team_uuid,
    ):
        result = db.session.query(
                Fine.label,
                func.count(PlayerFines.fine_uuid)
            ).join(
                PlayerFines, (Fine.uuid==PlayerFines.fine_uuid)
            ).filter(
                Fine.team_uuid==team_uuid,
            ).group_by(
                Fine.label
            ).order_by(
                func.count(PlayerFines.fine_uuid).desc()
            ).first()
        if result:
            return {
                'label': result[0],
                'total': result[1]
            }
        else:
            return {}
