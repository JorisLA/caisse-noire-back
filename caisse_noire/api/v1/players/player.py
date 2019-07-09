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
        post_data = request.get_json()

        if not kwargs['current_user'].banker:
            self.response_object['status'] = 'failure'
            return jsonify(
                {'message': 'The current user is not authorized'}
            ), 403

        player = self.get_player_by_uuid(player_uuid=player_uuid)
        if not player:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Player not found'}), 404

        try:
            if 'fine_uuid' in post_data:
                fine = self.get_fine_by_uuid(fine_uuid=post_data['fine_uuid'])
                if not fine:
                    self.response_object['status'] = 'failure'
                    return jsonify({'message': 'Fine not found'}), 404
                self.response_object['player'] = self.update_player_fine(
                    player, fine)
            self.response_object['message'] = 'Player updated!'
        except exc.SQLAlchemyError as error:
            print(error)
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Internal server error'}), 500

        self.response_object['status'] = 'success'
        return jsonify({'total': self.response_object['player']['total']}), 200

    @cross_origin()
    @token_required
    def delete(
        self,
        player_uuid,
        *args,
        **kwargs
    ):
        post_data = request.get_json()

        if not kwargs['current_user'].banker:
            self.response_object['status'] = 'failure'
            return jsonify(
                {'message': 'The current user is not authorized'}
            ), 403

        player = self.get_player_by_uuid(player_uuid=player_uuid)
        if not player:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Player not found'}), 404

        try:
            self.delete_fine(
                player=player,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message': 'Internal server error'}), 500

        self.response_object['message'] = 'Player removed!'
        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 204
