import jwt
import datetime

from flask import current_app
from app import bcrypt


def auth_for(user):
    return basic_auth(user.uuid, user.team_uuid)


def basic_auth(uuid, team_uuid):
    token = jwt.encode(
        {
            'public_id': uuid,
            'team_uuid': team_uuid,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        },
        current_app.config['SECRET_KEY']
    )

    return token.decode('UTF-8')
