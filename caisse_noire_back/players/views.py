from caisse_noire_back import *

@app.route('/players', methods=['GET', 'POST'])
@token_required
def all_players(*args, **kwargs):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        db = get_db()
        db.execute(
            'insert into players (uuid, first_name, last_name) values (?, ?, ?)',
                [
                    str(uuid.uuid4()),
                    post_data['first_name'],
                    post_data['last_name']
                ]
        )
        db.commit()
        response_object['message'] = 'Player added!'
    else:
        PLAYERS = []
        FINES = []
        for player in query_db(
            " SELECT players.uuid, players.first_name, players.last_name, SUM(cost) as total\
                FROM players\
                LEFT JOIN players_fines on players.uuid = players_fines.player_uuid\
                LEFT JOIN fines on players_fines.fine_uuid = fines.uuid\
                GROUP BY players.uuid\
            "
        ):
            PLAYERS.append({
                'uuid': player['uuid'],
                'first_name': player['first_name'],
                'last_name': player['last_name'],
                'total': player['total']
            })
        for fine in query_db('select * from fines'):
            FINES.append({
                'value': fine['uuid'],
                'text': fine['label']
            })
        response_object['players'] = PLAYERS
        response_object['fines'] = FINES
    return jsonify(response_object)

@app.route('/players/<player_uuid>', methods=['PUT', 'DELETE'])
@token_required
def single_player(player_uuid, *args, **kwargs):
    response_object = {'status': 'success'}
    if request.method == 'PUT' and kwargs['current_user']['banker'] == 1::
        post_data = request.get_json()
        db = get_db()
        db.execute(
            'update players set first_name = ?, last_name = ? where uuid = ?',
                [
                    post_data['first_name'],
                    post_data['last_name'],
                    player_uuid
                ]
        )
        db.execute(
            'insert into players_fines (uuid, player_uuid, fine_uuid) values (?, ?, ?)',
                [
                    str(uuid.uuid4()),
                    player_uuid,
                    post_data['fine_uuid']
                ]
        )
        db.commit()
        response_object['message'] = 'Player updated!'
    if request.method == 'DELETE':
        remove_player(player_uuid)
        response_object['message'] = 'Player removed!'
    return jsonify(response_object)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@token_required
def remove_player(player_uuid, *args, **kwargs):
    if request.method == 'DELETE' and kwargs['current_user']['banker'] == 1::
        db = get_db()
        db.execute('delete from players where uuid = ?', [player_uuid])
        db.commit()
