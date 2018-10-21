from app import *

@app.route('/players', methods=['GET', 'POST'])
@cross_origin()
@token_required
def all_players(*args, **kwargs):
    response_object = {'status': 'success'}
    if request.method == 'POST':
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
        response_object['message'] = 'Player added!'
    else:
        PLAYERS = []
        FINES = []

        players = db.session.query(
                func.sum(Fine.cost).label('total'),
                Player.uuid,
                Player.first_name,
                Player.last_name
            ).join(
                PlayerFines, (Fine.uuid==PlayerFines.c.fine_uuid)
            ).join(
                Player, (PlayerFines.c.player_uuid==Player.uuid)
            ).join(
                Team, (Player.team_uuid==Team.uuid)
            ).filter(
                Team.uuid == kwargs['current_user'].team_uuid
            ).group_by(
                Player.uuid
            )
        fines = Fine.query.all()
        for player in players:
            PLAYERS.append({
                'uuid': player.uuid,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'total': player.total
            })
        for fine in fines:
            FINES.append({
                'value': fine.uuid,
                'text': fine.label
            })
        response_object['players'] = PLAYERS
        response_object['fines'] = FINES
    return jsonify(response_object)

@app.route('/players/<player_uuid>', methods=['PUT', 'DELETE'])
@cross_origin()
@token_required
def single_player(player_uuid, *args, **kwargs):
    response_object = {'status': 'success'}
    if request.method == 'PUT' and kwargs['current_user'].banker == 1:
        post_data = request.get_json()
        player = Player.query.filter_by(uuid=player_uuid).first()
        player.first_name = post_data['first_name']
        player.last_name = post_data['last_name']
        if 'fine_uuid' in post_data:
            fine = Fine.query.filter_by(uuid=post_data['fine_uuid']).first()
            fine.players_fines.append(player)
        db.session.commit()
        response_object['message'] = 'Player updated!'
    if request.method == 'DELETE' and kwargs['current_user'].banker == 1:
        db.session.delete(Player.query.filter_by(uuid=player_uuid).first())
        db.session.commit()
        response_object['message'] = 'Player removed!'
    return jsonify(response_object)

# sanity check route
@app.route('/ping', methods=['GET'])
@cross_origin()
def ping_pong():
    return jsonify('pong!')

