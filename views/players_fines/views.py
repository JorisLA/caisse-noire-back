from flask.views import MethodView

from app import (
    cross_origin,
    app,
    request,
    jsonify,
    mail
)
from common.decorators.identification_authorizer import token_required
from models.repository.player_repository import PlayerModelRepository

class BillApi(
    MethodView,
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
        response_object = {'status': 'success'}
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
        response_object = {'status': 'success'}
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
        response_object = {'status': 'success'}
        if kwargs['current_user'].banker == 1:
            player = self.get_player_by_uuid(player_uuid=player_uuid)
            self.delete_player_fines(player=player)
            return '', 204


app.add_url_rule('/bills', view_func=BillApi.as_view('bills'))
app.add_url_rule('/bills/<player_uuid>', view_func=BillApi.as_view('bill'))