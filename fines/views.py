from app import *
from flask.views import MethodView

class FineApi(MethodView):

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
            return jsonify({'message' : 'The current user is not authorized'}), 403

        if not post_data:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Empty data sent in the request'}), 400

        team = Team.get_team_by_uuid(team_uuid=kwargs['current_user'].team_uuid)
        if not team:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Team not found'}), 404
        try:
            Fine.create_fine(
                post_data=post_data,
                team=team,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Internal server error'}), 500

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
            self.response_object['fines'] = Fine.get_fines(
                user_team_uuid=kwargs['current_user'].team_uuid,
                _sort=_sort,
                _order=_order,
                _filter=_filter,
                _currentPage=_currentPage,
                _perPage=_perPage,
                _offset=_offset,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Internal server error'}), 500

        if not self.response_object['fines']:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'No fines or wrong team uuid'}), 404

        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 200


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
            return jsonify({'message' : 'The current user is not authorized'}), 403
        
        fine = Fine.get_fine_by_uuid(fine_uuid=fine_uuid)
        if not fine:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Fine not found'}), 404

        try:
            Fine.update_fine(
                post_data=post_data,
                fine=fine,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Internal server error'}), 500

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
            return jsonify({'message' : 'The current user is not authorized'}), 403

        fine = Fine.get_fine_by_uuid(fine_uuid=fine_uuid)
        if not fine:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Fine not found'}), 404

        try:
            Fine.delete_fine(
                fine=fine,
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Internal server error'}), 500

        self.response_object['message'] = 'Fine removed!'
        self.response_object['status'] = 'success'
        return jsonify(self.response_object), 204


app.add_url_rule('/fines', view_func=FineApi.as_view('fines'))
app.add_url_rule('/fines/<fine_uuid>', view_func=FineApi.as_view('fine'))
