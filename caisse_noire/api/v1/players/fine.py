from flask.views import MethodView, View
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from caisse_noire.common.decorators.identification_authorizer import token_required
from caisse_noire.models.repository.player_repository import PlayerModelRepository
from app import mail

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
        self.response_object['fines']  = self.get_player_fines(player_uuid=player_uuid)
        return jsonify(self.response_object), 200

    @cross_origin()
    @token_required
    def delete(
        self,
        player_uuid,
        *args,
        **kwargs
    ):
        if kwargs['current_user'].banker == 1:
            player = self.get_player_by_uuid(player_uuid=player_uuid)
            self.delete_player_fines(player=player)
            return '', 204
