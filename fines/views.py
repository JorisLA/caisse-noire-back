from app import *

@app.route('/fines', methods=['GET', 'POST'])
@cross_origin()
@token_required
def all_fines(*args, **kwargs):
    response_object = {'status': 'success'}
    if request.method == 'POST' and kwargs['current_user'].banker == 1:
        post_data = request.get_json()
        fine = Fine(
            uuid=str(uuid.uuid4()),
            label=post_data['label'],
            cost=post_data['cost']
        )
        db.session.add(fine)
        team = Team.query.filter_by(uuid=kwargs['current_user'].team_uuid).first()
        fine.teams_fines.append(team)
        db.session.commit()
        response_object['message'] = 'Fine added!'
    else:
        FINES = []
        fines = db.session.query(
            Fine.uuid,
            Fine.label,
            Fine.cost,
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
                'uuid': fine.uuid,
                'label': fine.label,
                'cost': fine.cost
            })
        response_object['fines'] = FINES
    return jsonify(response_object)

@app.route('/fines/<fine_uuid>', methods=['PUT', 'DELETE'])
@cross_origin()
@token_required
def single_fine(fine_uuid, *args, **kwargs):
    response_object = {'status': 'success'}
    if request.method == 'PUT' and kwargs['current_user'].banker == 1:
        post_data = request.get_json()
        fine = Fine.query.filter_by(uuid=fine_uuid).first()
        fine.label = post_data['label']
        fine.cost = post_data['cost']
        db.session.commit()
        response_object['message'] = 'Fine updated!'
    if request.method == 'DELETE' and kwargs['current_user'].banker == 1:
        db.session.delete(Fine.query.filter_by(uuid=fine_uuid).first())
        db.session.commit()
        response_object['message'] = 'Fine removed!'
    return jsonify(response_object)
