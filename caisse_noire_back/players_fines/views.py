from caisse_noire_back import *

@app.route('/bills', methods=['DELETE'])
@token_required
def send_bills(*args, **kwargs):
    response_object = {'status': 'success'}
    PLAYERS = []
    if request.method == 'DELETE' and kwargs['current_user']['banker'] == 1:
        db = get_db()
        db.execute('DELETE FROM players_fines')
        db.commit()
    return '', 204