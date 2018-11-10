from app import *

@app.route('/bills', methods=['DELETE'])
@cross_origin()
@token_required
def send_bills(*args, **kwargs):
    response_object = {'status': 'success'}
    PLAYERS = []
    if request.method == 'DELETE' and kwargs['current_user'].banker == 1:       
        players = Player.query.filter_by(team_uuid=kwargs['current_user'].team_uuid).all()
        for player in players:
            player.fines = []
        db.session.commit()
        # send single recipient; single email as string
        #mail.send_email(
        #    from_email='joris.laruelle83@gmail.com',
        #    to_email='joris.laruelle83@gmail.com',
        #    subject='Subject',
        #    text='Body'
        #)
        return '', 204