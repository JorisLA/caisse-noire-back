
from flask.views import MethodView, View
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from caisse_noire.common.decorators.identification_authorizer import (
    token_required
)
from caisse_noire.models.repository.team_repository import TeamModelRepository
from caisse_noire.models.repository.fine_repository import FineModelRepository
from caisse_noire.common.exceptions.database_exceptions import (
    ModelCreationError,
    EntityNotFound,
)
from caisse_noire.common.exceptions.authorization_exceptions import (
    AuthorizationError,
)
from caisse_noire.common.settings import MAX_PER_PAGE


class FineHandler(
    MethodView,
    View,
    FineModelRepository,
    TeamModelRepository,
):

    def __init__(
            self,
    ):
        self.response_object = {}

    @cross_origin()
    @token_required
    def put(
        self,
        fine_uuid,
        *args,
        **kwargs
    ):
        payload = {
            'banker': kwargs['current_user'].banker,
            'label': request.get_json().get('label'),
            'cost': request.get_json().get('cost'),
            'fine_uuid': fine_uuid,
        }

        try:
            self.update_fine(payload=payload)
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
        except ModelCreationError as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 422
        except exc.SQLAlchemyError as e:
            return jsonify(
                {
                    'message': f'{e.error_code}'
                }
            ), 500

        self.response_object['message'] = 'Fine updated!'
        return jsonify(self.response_object), 204

    @cross_origin()
    @token_required
    def delete(
        self,
        fine_uuid,
        *args,
        **kwargs
    ):
        payload = {
            'banker': kwargs['current_user'].banker,
            'fine_uuid': fine_uuid,
        }

        try:
            self.delete_fine(
                payload=payload,
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
        except exc.SQLAlchemyError as e:
            return jsonify(
                {
                    'message': f'{e.error_code}'
                }
            ), 500

        self.response_object['message'] = 'Fine removed!'
        return jsonify(self.response_object), 204
