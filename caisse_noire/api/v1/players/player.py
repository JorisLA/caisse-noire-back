import uuid

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
from caisse_noire.models.repository.fine_repository import (
    FineModelRepository
)
from caisse_noire.common.exceptions.database_exceptions import (
    ModelCreationError,
    EntityNotFound,
)
from caisse_noire.common.exceptions.authorization_exceptions import (
    AuthorizationError,
)
from caisse_noire.common.settings import MAX_PER_PAGE


class PlayerHandler(
    MethodView,
    View,
    PlayerModelRepository,
    FineModelRepository,
):

    def __init__(
            self,
    ):
        self.response_object = {}

    @cross_origin()
    @token_required
    def put(
        self,
        player_uuid,
        *args,
        **kwargs
    ):
        payload = {
            'banker': kwargs['current_user'].banker,
            'player_uuid': player_uuid,
            'fine_uuid': (
                request.get_json()['fine_uuid']
                if request.get_json()
                else None
            ),
        }
        try:
            self.response_object['player'] = self.update_player_fine(payload)
            self.response_object['message'] = 'Player updated!'
        except AuthorizationError as e:
            self.response_object['status'] = 'failure'
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 403
        except EntityNotFound as e:
            self.response_object['status'] = 'failure'
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 404
        except ModelCreationError as e:
            self.response_object['status'] = 'failure'
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 422
        except exc.SQLAlchemyError as e:
            self.response_object['status'] = 'failure'
            return jsonify(
                {
                    'message': f'{e.error_code}'
                }
            ), 500

        self.response_object['status'] = 'success'
        return jsonify({'total': self.response_object['player']['total']}), 200
