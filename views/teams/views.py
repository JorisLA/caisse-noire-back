import uuid

from flask.views import MethodView

from app import (
    cross_origin,
    app,
    request,
    jsonify
)
from common.decorators.identification_authorizer import token_required
from models.repository.team_repository import TeamModelRepository

class TeamApi(
    MethodView,
    TeamModelRepository,
):

    def __init__(
            self,
    ):
        self.response_object = {}

    @cross_origin()
    def post(
        self,
        *args,
        **kwargs
    ):
        post_data = request.get_json()
        team = Team(
            uuid=str(uuid.uuid4()),
            label=post_data['label']
        )
        db.session.add(team)
        db.session.commit()
        return '', 204


    @cross_origin()
    def get(
        self,
        *args,
        **kwargs
    ):
        self.response_object = {}
        self.response_object['teams'] = self.get_teams()
        return jsonify(self.response_object)

app.add_url_rule('/teams', view_func=TeamApi.as_view('teams'))
