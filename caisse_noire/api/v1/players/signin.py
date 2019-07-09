import jwt
import datetime

from flask import request, jsonify
from flask.views import MethodView, View
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from caisse_noire.models.repository.player_repository import (
    PlayerModelRepository
)
from caisse_noire.common.exceptions.database_exceptions import (
    ModelCreationError,
    EntityNotFound,
)


class SigninHandler(
    MethodView,
    View,
    PlayerModelRepository
):

    @cross_origin()
    def post(
        self,
        *args,
        **kwargs
    ):
        try:
            return self.signin_player(request.get_json())
        except ModelCreationError as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 422
        except EntityNotFound as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 404
