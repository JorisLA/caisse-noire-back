import uuid

from flask.views import MethodView

from app import (
    cross_origin,
    app,
    request,
    jsonify,
    bcrypt,
)
from common.decorators.identification_authorizer import token_required
from models.repository.player_repository import PlayerModelRepository
from models.repository.team_repository import TeamModelRepository

class SignupApi(
    MethodView,
    PlayerModelRepository,
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
        pw_hash = bcrypt.generate_password_hash(post_data['password']).decode('utf-8')
        if 'add_team' in post_data:
            banker = True
            team_uuid = self.create_team(team_name=post_data['add_team'])
        else:
            team_uuid = post_data['get_team']
            team = self.get_team_by_uuid(team_uuid=team_uuid)
            banker = False
        post_data['pw_hash'] = pw_hash
        post_data['banker'] = banker
        post_data['team_uuid'] = team_uuid
        self.create_player(post_data)
        return '', 204

app.add_url_rule('/signup', view_func=SignupApi.as_view('signup'))
