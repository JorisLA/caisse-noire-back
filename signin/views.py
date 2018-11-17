from app import *
from flask.views import MethodView

class SigninApi(MethodView):

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
        player = Player.get_player_by_email(player_email=post_data['email'])
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
