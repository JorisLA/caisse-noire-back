from flask.views import MethodView
import sendgrid
from sendgrid.helpers.mail import *

from app import (
    cross_origin,
    app,
    request,
    jsonify,
    mail,
    os
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
        PLAYERS = []
        if kwargs['current_user'].banker == 1:
            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email("test@example.com")
            subject = "Hello World from the SendGrid Python Library!"
            to_email = Email("joris.laruelle83@gmail.com")
            content = Content("text/plain", "Hello, Email!")
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            # send single recipient; single email as string
            #mail.send_email(
            #    from_email='joris.laruelle83@gmail.com',
            #    to_email='joris.laruelle83@gmail.com',
            #    subject='Subject',
            #    text='Body'
            #)
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