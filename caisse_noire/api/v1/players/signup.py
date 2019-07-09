from flask import request, jsonify
from flask.views import MethodView, View
from flask_cors import cross_origin

from caisse_noire.models.repository.player_repository import (
    PlayerModelRepository
)
from caisse_noire.common.exceptions.database_exceptions import (
    ModelCreationError,
    EntityNotFound,
)


class SignupHandler(
    MethodView,
    View,
    PlayerModelRepository,
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
            player_uuid = self.signup_player(request.get_json())
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

        return '', 204
