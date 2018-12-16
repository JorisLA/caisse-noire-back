import uuid

from flask.views import MethodView

from app import (
    cross_origin,
    app,
    request,
    jsonify,
    exc,
)
from common.decorators.identification_authorizer import token_required
from models.repository.player_repository import PlayerModelRepository
from models.repository.fine_repository import FineModelRepository

class PlayerApi(
    MethodView,
    PlayerModelRepository,
    FineModelRepository,
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
        #db = get_db()
        #db.execute(
        #    'insert into players (uuid, first_name, last_name) values (?, ?, ?)',
        #        [
        #            str(uuid.uuid4()),
        #            post_data['first_name'],
        #            post_data['last_name']
        #        ]
        #)
        #db.commit()
        self.response_object['message'] = 'Player added!'
        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 201


    @cross_origin()
    @token_required
    def get(
        self,
        *args,
        **kwargs
    ):
        PLAYERS = []
        FINES = []
        _sort = request.args.get('_sort')
        _order = request.args.get('_order')
        _filter = request.args.get('_filter')
        _currentPage = request.args.get('_currentPage')
        _perPage = request.args.get('_perPage')
        if _currentPage and _perPage:
            _offset = int(_perPage) * (int(_currentPage) - 1)
        else:
            _offset = 0

        try:
            self.response_object['players'] = self.get_players(
                team_uuid=kwargs['current_user'].team_uuid,
                _sort=_sort,
                _order=_order,
                _filter=_filter,
                _currentPage=_currentPage,
                _perPage=_perPage,
                _offset=_offset,
            )
            self.response_object['full_count'] = len(self.response_object['players'])
            self.response_object['fines'] = self.get_fines(
                user_team_uuid=kwargs['current_user'].team_uuid,
                _sort=_sort,
                _order=_order,
                _filter=_filter,
                _currentPage=_currentPage,
                _perPage=_perPage,
                _offset=_offset,
                for_player_view=True,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Internal server error'}), 500

        return jsonify(self.response_object), 200


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
            return jsonify({'message' : 'The current user is not authorized'}), 403

        player = self.get_player_by_uuid(player_uuid=player_uuid)
        if not player:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Player not found'}), 404

        try:
            if 'fine_uuid' in post_data:
                fine = self.get_fine_by_uuid(fine_uuid=post_data['fine_uuid'])
                if not fine:
                    self.response_object['status'] = 'failure'
                    return jsonify({'message' : 'Fine not found'}), 404
                self.update_player_fine(player, fine)
            self.response_object['message'] = 'Player updated!'
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Internal server error'}), 500

        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 204


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
            return jsonify({'message' : 'The current user is not authorized'}), 403

        player = self.get_player_by_uuid(player_uuid=player_uuid)
        if not player:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Player not found'}), 404

        try:
            self.delete_fine(
                player=player,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Internal server error'}), 500

        self.response_object['message'] = 'Player removed!'
        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 204

app.add_url_rule('/players', view_func=PlayerApi.as_view('players'))
app.add_url_rule('/players/<player_uuid>', view_func=PlayerApi.as_view('player'))
