from flask.views import MethodView

from app import (
    cross_origin,
    app,
    request,
    jsonify,
    exc, 
)
from common.decorators.identification_authorizer import token_required
from models.repository.team_repository import TeamModelRepository
from models.repository.fine_repository import FineModelRepository
from common.settings import MAX_PER_PAGE

class FineApi(
    MethodView,
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
            return jsonify({'message' : 'The current user is not authorized'}), 403

        if not post_data:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Empty data sent in the request'}), 400

        team = self.get_team_by_uuid(team_uuid=kwargs['current_user'].team_uuid)
        if not team:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Team not found'}), 404
        try:
            self.create_fine(
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
        additional_filters = {
            'sort':request.args.get('_sort', None),
            'order':request.args.get('_order', None),
            'filter':request.args.get('_filter', None),
            'currentPage':request.args.get('_currentPage', 1),
            'perPage':request.args.get('_perPage', MAX_PER_PAGE),
            'lastUuid':request.args.get('_lastUuid', None),
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
            return jsonify({'message' : 'Internal server error'}), 500

        # if not self.response_object['fines']:
        #     self.response_object['status'] = 'failure'
        #     return jsonify({'message' : 'No fines or wrong team uuid'}), 404

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
        
        fine = self.get_fine_by_uuid(fine_uuid=fine_uuid)
        if not fine:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Fine not found'}), 404

        try:
            self.update_fine(
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

        fine = self.get_fine_by_uuid(fine_uuid=fine_uuid)
        if not fine:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Fine not found'}), 404

        try:
            self.delete_fine(
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
