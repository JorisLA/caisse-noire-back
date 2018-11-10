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
        _sort = request.args.get('_sort')
        _order = request.args.get('_order')
        _filter = request.args.get('_filter')
        _currentPage = request.args.get('_currentPage')
        _perPage = request.args.get('_perPage')
        if _currentPage and _perPage:
            _offset = int(_perPage) * (int(_currentPage) - 1)
        if _sort and _order:
            query = text(
                """
                SELECT sum(fine.cost) AS total,
                    player.uuid,
                    player.first_name,
                    player.last_name,
                    count(*) OVER() AS full_count
                        FROM player
                        LEFT OUTER JOIN "PlayerFines" ON player.uuid = "PlayerFines".player_uuid
                        LEFT OUTER JOIN fine ON "PlayerFines".fine_uuid = fine.uuid
                        JOIN team ON player.team_uuid = team.uuid
                            WHERE team.uuid = :team_uuid
                            GROUP BY player.uuid
                            ORDER BY {0} {1}
                            OFFSET :_offset
                """.format(_sort, _order)
            )
            players = db.engine.execute(
                query,
                team_uuid=kwargs['current_user'].team_uuid,
                _offset=_offset,
            ).fetchall()
        elif _filter:
            query = text(
                """
                SELECT sum(fine.cost) AS total,
                    player.uuid,
                    player.first_name,
                    player.last_name,
                    count(*) OVER() AS full_count
                        FROM player
                        LEFT OUTER JOIN "PlayerFines" ON player.uuid = "PlayerFines".player_uuid
                        LEFT OUTER JOIN fine ON "PlayerFines".fine_uuid = fine.uuid
                        JOIN team ON player.team_uuid = team.uuid
                            WHERE team.uuid = :team_uuid
                            AND (player.first_name LIKE :_filter OR player.last_name LIKE :_filter)
                            GROUP BY player.uuid
                """
            )
            players = db.engine.execute(
                query,
                team_uuid=kwargs['current_user'].team_uuid,
                _filter='%' + _filter + '%',
            ).fetchall()
        elif int(_currentPage) > 1:
            query = text(
                """
                SELECT sum(fine.cost) AS total,
                    player.uuid,
                    player.first_name,
                    player.last_name,
                    count(*) OVER() AS full_count
                        FROM player
                        LEFT OUTER JOIN "PlayerFines" ON player.uuid = "PlayerFines".player_uuid
                        LEFT OUTER JOIN fine ON "PlayerFines".fine_uuid = fine.uuid
                        JOIN team ON player.team_uuid = team.uuid
                            WHERE team.uuid = :team_uuid
                            GROUP BY player.uuid
                            OFFSET :_offset
                """
            )
            players = db.engine.execute(
                query,
                team_uuid=kwargs['current_user'].team_uuid,
                _offset=_offset,
            ).fetchall()
        else:
            query = text(
                """
                SELECT sum(fine.cost) AS total,
                    player.uuid,
                    player.first_name,
                    player.last_name,
                    count(*) OVER() AS full_count
                        FROM player
                        LEFT OUTER JOIN "PlayerFines" ON player.uuid = "PlayerFines".player_uuid
                        LEFT OUTER JOIN fine ON "PlayerFines".fine_uuid = fine.uuid
                        JOIN team ON player.team_uuid = team.uuid
                            WHERE team.uuid = :team_uuid
                            GROUP BY player.uuid
                            LIMIT :_perPage
                """
            )
            players = db.engine.execute(
                query,
                team_uuid=kwargs['current_user'].team_uuid,
                _perPage=_perPage,
            ).fetchall()
        fines = db.session.query(
            Fine.uuid,
            Fine.label,
            TeamFines.c.team_uuid
            ).join(
                TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
            ).filter(
                TeamFines.c.team_uuid == kwargs['current_user'].team_uuid
            ).group_by(
                TeamFines.c.team_uuid,
                Fine.uuid
            )
        for fine in fines:
            FINES.append({
                'value': fine.uuid,
                'text': fine.label
            })
        for player in players:
            PLAYERS.append({
                'uuid': player.uuid,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'total': player.total,
                'full_count': player.full_count
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
        if 'fine_uuid' in post_data:
            fine = Fine.query.filter_by(uuid=post_data['fine_uuid']).first()
            association = PlayerFines(player_fines_id=str(uuid.uuid4()))
            association.fine = fine
            player.fines.append(association)
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

