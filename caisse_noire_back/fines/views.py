from caisse_noire_back import *

@app.route('/fines', methods=['GET', 'POST'])
@token_required
def all_fines(*args, **kwargs):
    response_object = {'status': 'success'}
    if request.method == 'POST' and kwargs['current_user']['banker'] == 1:
        post_data = request.get_json()
        db = get_db()
        db.execute('insert into fines (uuid, label, cost) values (?, ?, ?)',
                    [str(uuid.uuid4()), post_data['label'], post_data['cost']])
        db.commit()
        response_object['message'] = 'Fine added!'
    else:
        FINES = []
        for fine in query_db('select * from fines'):
            FINES.append({
                'uuid': fine['uuid'],
                'label': fine['label'],
                'cost': fine['cost']
            })
        response_object['fines'] = FINES
    return jsonify(response_object)

@app.route('/fines/<fine_uuid>', methods=['PUT', 'DELETE'])
@token_required
def single_fine(fine_uuid, *args, **kwargs):
    response_object = {'status': 'success'}
    if request.method == 'PUT' and kwargs['current_user']['banker'] == 1:
        post_data = request.get_json()
        db = get_db()
        db.execute('update fines set label = ?, cost = ? where uuid = ?',
            [post_data['label'], post_data['cost'], fine_uuid])
        db.commit()
        response_object['message'] = 'Fine updated!'
    if request.method == 'DELETE' and kwargs['current_user']['banker'] == 1::
        remove_fine(fine_uuid)
        response_object['message'] = 'Fine removed!'
    return jsonify(response_object)

@token_required
def remove_fine(fine_uuid, *args, **kwargs):
    if request.method == 'DELETE' and kwargs['current_user']['banker'] == 1:
        db = get_db()
        db.execute('delete from fines where uuid = ?', [fine_uuid])
        db.commit()
    return False