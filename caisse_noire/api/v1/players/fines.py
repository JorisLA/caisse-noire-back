from flask.views import MethodView, View
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from caisse_noire.common.decorators.identification_authorizer import token_required
from caisse_noire.models.repository.player_repository import PlayerModelRepository
from app import mail

class PlayersFinesHandler(
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

