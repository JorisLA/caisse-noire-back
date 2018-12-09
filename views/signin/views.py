import jwt
import datetime

from flask.views import MethodView

from app import (
    cross_origin,
    app,
    request,
    jsonify,
    bcrypt,
)
from common.decorators.identification_authorizer import token_required
from models.repository.team_repository import TeamModelRepository
from models.repository.player_repository import PlayerModelRepository

class SigninApi(
    MethodView,
    TeamModelRepository,
    PlayerModelRepository,
):

    def __init__(
            self,
    ):
        self.response_object = {}

    @cross_origin()
    def post(
        self,
        *args,
        **kwargs
    ):
        post_data = request.get_json()
        player = self.get_player_by_email(player_email=post_data['email'])
        if player is None:
            self.response_object['status'] = 'failure'
            return jsonify({'message' : 'Player not found'}), 404
        else:
            if bcrypt.check_password_hash(player.password, post_data['password']):
                # auth = request.authorization

                # if not auth or not auth.email or not auth.password:
                #    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

                token = jwt.encode(
                    {
                        'public_id' : player.uuid,
                        'team_uuid' : player.team_uuid,
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                    },
                    app.config['SECRET_KEY']
                )

                return jsonify(
                        {
                            'token' : token.decode('UTF-8'),
                            'banker' : player.banker,
                        }
                    )

app.add_url_rule('/signin', view_func=SigninApi.as_view('signin'))
