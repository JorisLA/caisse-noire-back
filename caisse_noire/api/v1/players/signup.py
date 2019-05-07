import uuid
import jwt
import datetime

from flask import request, jsonify, current_app
from flask.views import MethodView, View
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from caisse_noire.common.decorators.identification_authorizer import token_required
from caisse_noire.models.repository.player_repository import PlayerModelRepository
from caisse_noire.models.repository.team_repository import TeamModelRepository
from app import bcrypt

class SignupHandler(
    MethodView,
    View,
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
        player_uuid = self.create_player(post_data)
        token = jwt.encode(
            {
                'public_id' : player_uuid,
                'team_uuid' : team_uuid,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            current_app.config['SECRET_KEY']
        )

        return jsonify(
                {
                    'token' : token.decode('UTF-8'),
                    'banker' : banker,
                }
            )
        # return '', 204
