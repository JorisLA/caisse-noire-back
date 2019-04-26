from flask.views import MethodView, View
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from flask_sendgrid import SendGrid
from sqlalchemy import exc

from common.decorators.identification_authorizer import token_required
from models.repository.player_repository import PlayerModelRepository
from views.base_handler import BaseHandler

mail = SendGrid()

class BillApi(
    MethodView,
    View,
    PlayerModelRepository,
    BaseHandler
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
        if kwargs['current_user'].banker == 1:
            players = self.get_players_by_team(team_uuid=kwargs['current_user'].team_uuid)
            for player in players:
                fine_cost = self.get_player_fine_cost(player_uuid=player.uuid)
                mail.send_email(
                    from_email='admin@caissenoire.com',
                    to_email=player.email,
                    subject='Caisse noire payment',
                    text='You have to pay {} € this month'.format(fine_cost),
                )
        return '', 204

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
