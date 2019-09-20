
from flask.views import MethodView, View
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from caisse_noire.common.decorators.identification_authorizer import(
    token_required
)
from caisse_noire.common.exceptions.authorization_exceptions import (
    AuthorizationError,
)
from caisse_noire.common.exceptions.database_exceptions import (
    ModelCreationError,
    EntityNotFound,
)
from caisse_noire.models.team import Team
from caisse_noire.models.repository.team_repository import TeamModelRepository
from caisse_noire.models.repository.fine_repository import FineModelRepository
from caisse_noire.common.settings import MAX_PER_PAGE


class FinesHandler(
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
    def post(
        self,
        *args,
        **kwargs
    ):
        try:
            self.create_fine(
                banker=kwargs['current_user'].banker,
                post_data=request.get_json(),
                team_uuid=kwargs['current_user'].team_uuid,
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
        except ModelCreationError as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 422
        except exc.SQLAlchemyError as e:
            self.response_object['status'] = 'failure'
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 500

        self.response_object['message'] = 'Fine added!'
        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 201

    @cross_origin()
    @token_required
    def get(
        self,
        *args,
        **kwargs
    ):
        filters = {
            'sort': request.args.get('_sort', None),
            'order': request.args.get('_order', None),
            'filter': request.args.get('_filter', None),
            'currentPage': request.args.get('_currentPage', 1),
            'perPage': request.args.get('_perPage', MAX_PER_PAGE),
            'lastUuid': request.args.get('_lastUuid', None),
        }
        try:
            results = self.get_all_fines_by_team(
                team_uuid=kwargs['current_user'].team_uuid,
                filters=filters,
            )
            self.response_object['fines'] = [
                fine.to_dict()
                for fine in results['fines']
            ]
        except EntityNotFound as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 404
        except exc.SQLAlchemyError as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 500

        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 200
