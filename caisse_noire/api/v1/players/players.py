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
from caisse_noire.common.exceptions.database_exceptions import (
    ModelCreationError,
    EntityNotFound,
)
from caisse_noire.models.repository.fine_repository import FineModelRepository
from caisse_noire.common.settings import MAX_PER_PAGE


class PlayersHandler(
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
    def get(
        self,
        *args,
        **kwargs
    ):
        PLAYERS = []
        FINES = []
        additional_filters = {
            'sort': request.args.get('_sort', None),
            'order': request.args.get('_order', None),
            'filter': request.args.get('_filter', None),
            'currentPage': request.args.get('_currentPage', 1),
            'perPage': request.args.get('_perPage', MAX_PER_PAGE),
            'lastUuid': request.args.get('_lastUuid', None),
        }
        try:
            results = self.get_all_players_from_team(
                team_uuid=kwargs['current_user'].team_uuid,
                additional_filters=additional_filters
            )
            self.response_object['players'] = [
                player.to_dict()
                for player in results['players']
            ]
            self.response_object['full_count'] = results['total_rows']
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Internal server error'}), 500
        except EntityNotFound as e:
            return jsonify(
                {
                    'message': f'{e.error_code}',
                }
            ), 404

        return jsonify(self.response_object), 200
