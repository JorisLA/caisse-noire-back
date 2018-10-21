from app import *

@app.route('/teams', methods=['GET', 'POST'])
@cross_origin()
def create_team():
    if request.method == 'POST':
        post_data = request.get_json()
        team = Team(
            uuid=str(uuid.uuid4()),
            label=post_data['label']
        )
        db.session.add(team)
        db.session.commit()
        return '', 204
    else:
        TEAMS = []
        response_object = {}
        teams = Team.query.all()
        for team in teams:
            TEAMS.append({
                'value': team.uuid,
                'text': team.label,
            })
        response_object['teams'] = TEAMS
    return jsonify(response_object)