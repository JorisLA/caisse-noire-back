
from flask.views import MethodView, View
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import exc


class PingHandler(
    MethodView,
    View,
):

    def __init__(
            self,
    ):
        self.response_object = {}

    @cross_origin()
    def get(
        self,
        *args,
        **kwargs
    ):
        return 'ok'
