from app import *

@app.route('/teams', methods=['GET', 'POST'])
def create_team():
    if request.method == 'POST':
        post_data = request.get_json()
        db = get_db()
        db.execute(
            'INSERT INTO teams (uuid, label) values (?, ?)',
                [
                    str(uuid.uuid4()),
                    post_data['label'],
                ]
        )
        db.commit()
        return '', 204
    else:
        TEAMS = []
        response_object = {}
        for team in query_db(
            'SELECT * FROM teams'
        ):
            TEAMS.append({
                'value': team['uuid'],
                'text': team['label'],
            })
        response_object['teams'] = TEAMS
    return jsonify(response_object)