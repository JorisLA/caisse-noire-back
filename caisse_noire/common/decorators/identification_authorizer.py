import jwt

from functools import wraps
from flask import request, jsonify, current_app

from caisse_noire.models.player import Player
from app import db


def token_required(f):
    """
    Check identification through a token authorizer

    Args:
        authorizer_list (list): list of authorizer to use

    Returns:
        returns the decorated function or unauthorized http response
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'token_missing'}), 401

        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=['HS256']
            )
            current_user = db.session.query(Player).filter_by(
                uuid=data['public_id']
            ).first()
            kwargs['current_user'] = current_user
        except:
            return jsonify({'message': 'token_invalid'}), 401

        return f(*args, **kwargs)

    return decorated
