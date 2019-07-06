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
from caisse_noire.common.exceptions.database_exceptions import (
    DatabaseError,
    ModelCreationError,
    ModelUpdateError,
)


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
        try:
            player_uuid = self.create_player(request.get_json())
        except ModelCreationError as e:
            return jsonify(
                {
                    'message': 'cant_create_object{}'.format(e.error_code)
                }
            ), 400

        return '', 204
