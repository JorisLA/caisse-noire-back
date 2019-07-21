
from flask.views import MethodView, View
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from caisse_noire.common.decorators.identification_authorizer import (
    token_required
)
from caisse_noire.models.repository.team_repository import TeamModelRepository
from caisse_noire.models.repository.fine_repository import FineModelRepository
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
        post_data = request.get_json()

        if not kwargs['current_user'].banker:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'The current user is not authorized'}), 403

        fine = self.get_fine_by_uuid(fine_uuid=fine_uuid)
        if not fine:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Fine not found'}), 404

        try:
            self.update_fine(
                post_data=post_data,
                fine=fine,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Internal server error'}), 500

        self.response_object['message'] = 'Fine updated!'
        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 204

    @cross_origin()
    @token_required
    def delete(
        self,
        fine_uuid,
        *args,
        **kwargs
    ):
        post_data = request.get_json()

        if not kwargs['current_user'].banker:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'The current user is not authorized'}), 403

        fine = self.get_fine_by_uuid(fine_uuid=fine_uuid)
        if not fine:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Fine not found'}), 404

        try:
            self.delete_fine(
                fine=fine,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Internal server error'}), 500

        self.response_object['message'] = 'Fine removed!'
        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 204
