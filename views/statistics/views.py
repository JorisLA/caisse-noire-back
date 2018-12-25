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
from models.repository.team_repository import TeamModelRepository

class StatisticApi(
    MethodView,
    TeamModelRepository,
):

    def __init__(
            self,
    ):
        self.response_object = {}

    @cross_origin()
    @token_required
    def get(
        self,
        *args,
        **kwargs
    ):
        try:
            self.response_object['bestContributor'] = self.get_best_contributor(
                kwargs['current_user'].team_uuid
            )
            self.response_object['mostRecurrentFine'] = self.get_most_recurrent_fine(
                kwargs['current_user'].team_uuid
            )
        except exc.SQLAlchemyError as error:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Internal server error'}), 500


        if not self.response_object['bestContributor'] or not self.response_object['mostRecurrentFine']:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'No statistic'}), 404

        return jsonify(self.response_object), 200

app.add_url_rule('/statistic', view_func=StatisticApi.as_view('statistics'))
