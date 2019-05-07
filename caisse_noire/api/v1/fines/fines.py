
from flask.views import MethodView, View
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from caisse_noire.common.decorators.identification_authorizer import token_required
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
        post_data = request.get_json()

        if not kwargs['current_user'].banker:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'The current user is not authorized'}), 403

        if not post_data:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Empty data sent in the request'}), 400

        team = self.get_team_by_uuid(
            team_uuid=kwargs['current_user'].team_uuid)
        if not team:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Team not found'}), 404
        try:
            self.create_fine(
                post_data=post_data,
                team=team,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Internal server error'}), 500

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
        additional_filters = {
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
                additional_filters=additional_filters,
            )
            self.response_object['fines'] = [
                fine.to_dict()
                for fine in results['fines']
            ]
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Internal server error'}), 500

        # if not self.response_object['fines']:
        #     self.response_object['status'] = 'failure'
        #     return jsonify({'message' : 'No fines or wrong team uuid'}), 404

        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 200

