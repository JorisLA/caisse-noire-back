from flask.views import MethodView, View
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from caisse_noire.common.decorators.identification_authorizer import (
    token_required
)
from caisse_noire.models.repository.player_repository import (
    PlayerModelRepository
)
from app import mail


class PlayersFinesHandler(
    MethodView,
    View,
    PlayerModelRepository,
):

    def __init__(
            self,
    ):
        self.response_object = {}

    @cross_origin()
    @token_required
    def post(
        self,
        *args,
        **kwargs
    ):
        player_email = []
        try:
            self.send_fines_to_players_email(
                banker=kwargs['current_user'].banker,
                team_uuid=team_uuid,
            )
        except AuthorizationError as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 403
        except EntityNotFound as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 404

        return '', 204
