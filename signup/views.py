from app import *
from flask.views import MethodView

class SignupApi(MethodView):

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
        pw_hash = bcrypt.generate_password_hash(post_data['password']).decode('utf-8')
        if 'add_team' in post_data:
            banker = True
            team_uuid = str(uuid.uuid4())
            team = Team(uuid=team_uuid, label=post_data['add_team'])
            db.session.add(team)
        else:
            team_uuid = post_data['get_team']
            team = Team.get_team_by_uuid(team_uuid=team_uuid)
            banker = False
        player = Player(
            uuid=str(uuid.uuid4()),
            first_name=post_data['first_name'],
            last_name=post_data['last_name'],
            email=post_data['email'],
            password=pw_hash,
            banker=banker,
            team_uuid=team_uuid,
        )
        db.session.add(player)
        db.session.commit()
        return '', 204

app.add_url_rule('/signup', view_func=SignupApi.as_view('signup'))
