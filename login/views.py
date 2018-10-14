from app import (
    app,
    request,
    get_db,
    bcrypt,
    uuid,
    query_db,
    jsonify,
    uuid,
    make_response,
    jwt,
    datetime
)

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        post_data = request.get_json()
        pw_hash = bcrypt.generate_password_hash(post_data['password']).decode('utf-8')
        db = get_db()
        if 'add_team' in post_data:
            team_uuid = str(uuid.uuid4())
            banker = 1
            db.execute(
                'INSERT INTO teams (uuid, label) values (?, ?)',
                    [
                        team_uuid,
                        post_data['add_team'],
                    ]
            )
        else:
            team_uuid = post_data['get_team']
            banker = 0
        db.execute(
            'INSERT INTO players (uuid, first_name, last_name, email, password, banker, team_uuid)\
                values (?, ?, ?, ?, ?, ?, ?)',
                    [
                        str(uuid.uuid4()),
                        post_data['first_name'],
                        post_data['last_name'],
                        post_data['email'],
                        pw_hash,
                        banker,
                        team_uuid,
                    ]
        )
        db.commit()
    return '', 204

@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        post_data = request.get_json()
        player = query_db('SELECT * FROM players WHERE email = ?',
            [
                post_data['email']
            ],
            one=True,
        )
        if player is None:
            return 'Player not exist', 404
        else:
            if bcrypt.check_password_hash(player['password'], post_data['password']):
                # auth = request.authorization

                # if not auth or not auth.email or not auth.password:
                #    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

                token = jwt.encode(
                    {
                        'public_id' : player['uuid'],
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                    },
                    app.config['SECRET_KEY']
                )

                return jsonify(
                        {
                            'token' : token.decode('UTF-8'),
                            'banker' : player['banker'],
                        }
                    )
