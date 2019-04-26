import uuid

from flask.views import MethodView
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask.views import View

from common.decorators.identification_authorizer import token_required
from models.repository.team_repository import TeamModelRepository
from models.team import Team
from views.base_handler import BaseHandler
from flask import current_app
db = SQLAlchemy(current_app)

class TeamApi(
    MethodView,
    View,
    TeamModelRepository,
    BaseHandler,
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
