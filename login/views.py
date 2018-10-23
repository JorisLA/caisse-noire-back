from app import *

@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    if request.method == 'POST':
        post_data = request.get_json()
        pw_hash = bcrypt.generate_password_hash(post_data['password']).decode('utf-8')
        if 'add_team' in post_data:
            banker = 1
            team_uuid = str(uuid.uuid4())
            team = Team(uuid=team_uuid, label=post_data['add_team'])
            db.session.add(team)
        else:
            team_uuid = post_data['get_team']
            team = Team.query.filter_by(uuid=team_uuid).first()
            banker = 0
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

@app.route('/signin', methods=['POST'])
@cross_origin()
def signin():
    if request.method == 'POST':
        post_data = request.get_json()
        player = Player.query.filter_by(email=post_data['email']).first()
        if player is None:
            return 'Player not exist', 404
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
