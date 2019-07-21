from flask.views import MethodView, View
from flask import jsonify
from flask_cors import cross_origin

from caisse_noire.common.decorators.identification_authorizer import (
    token_required,
)
from caisse_noire.models.repository.player_repository import (
    PlayerModelRepository,
)
from caisse_noire.common.exceptions.database_exceptions import (
    EntityNotFound,
)
from caisse_noire.common.exceptions.authorization_exceptions import (
    AuthorizationError,
)


class PlayerFineHandler(
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
    def get(
        self,
        player_uuid,
        *args,
        **kwargs
    ):
        try:
            self.response_object['fines'] = self.get_player_fines(
                player_uuid=player_uuid
            )
        except EntityNotFound as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 404
        return jsonify(self.response_object), 200

    @cross_origin()
    @token_required
    def delete(
        self,
        player_uuid,
        *args,
        **kwargs
    ):
        try:
            self.delete_player_fines(
                banker=kwargs['current_user'].banker,
                player_uuid=player_uuid,
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
