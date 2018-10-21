from app import *

@app.route('/bills', methods=['DELETE'])
@cross_origin()
@token_required
def send_bills(*args, **kwargs):
    response_object = {'status': 'success'}
    PLAYERS = []
    if request.method == 'DELETE' and kwargs['current_user'].banker == 1:
        try:
            num_rows_deleted = db.session.query(PlayerFines).delete()
            print(num_rows_deleted)
            db.session.commit()
        except:
            db.session.rollback()
    return '', 204