"""
Base handler class for every route
"""
import json
import uuid


class BaseHandler():

    def __init__(self, *args, **kwargs):
        self.db = None

    def initialize(self, **kwargs):
        self.db = kwargs['db']

    # def options(self, *args, **kwargs):
    #     self.finish()

    def prepare(self):
        self.db.create_session()

    def on_finish(self):
        self.db.close_session()

    # def return_success(
    #         self,
    #         json_data
    # ):
    #     """
    #     Return the object to the client
    #     Args:
    #         json_data: object to encode in JSON
    #     """
    #     if isinstance(json_data, list):
    #         # Tornado refuses to dump list into JSON by himself, dawn Tornado
    #         json_data = json.dumps(json_data)
    #         self.add_header('content-type', 'application/json')
    #     self.write(json_data)
    # 
    # def return_created(self, json_data):
    #     self.set_status(201, reason='')
    #     self.write(json_data)
    # 
    # def return_no_content(self):
    #     self.set_status(204, reason='')
    #     self.finish()
    # 
    # def return_error(
    #         self,
    #         http_code,
    #         error_code,
    #         params=None,
    # ):
    #     """
    #     Construct an error response object and return it to the client
    #     Args:
    #         http_code (int): Http error code
    #         error_code (str): Error message code
    #         params (list): Error Message params
    #     """
    #     if config.ACTIVATE_CORS_HEADERS:
    #         self.set_header(
    #             "Access-Control-Allow-Origin",
    #             config.CORS_HEADERS_ORIGIN,
    #         )
    #         self.set_header(
    #             "Access-Control-Allow-Headers",
    #             "x-requested-with, authorization, origin, content-type, accept",
    #         )
    #         self.set_header(
    #             'Access-Control-Allow-Methods',
    #             'POST, GET, OPTIONS, PUT, DELETE, OPTIONS, PATCH',
    #         )
    # 
    #     error_reason = build_error_response(error_code, params)
    # 
    #     log_message = {
    #         'http_code': http_code,
    #         'reason': error_reason
    #     }
    #     if error_code == 500:
    #         # 500 errors aren't suppose to happen
    #         self.logger.error(log_message)
    #     else:
    #         self.logger.warning(log_message)
    # 
    #     # reason is set to '' to workaround "bug" in python2.7
    #     # not handling 422 status code otherwise
    #     # see https://github.com/tornadoweb/tornado/issues/1751
    #     self.set_status(http_code, reason='')
    #     self.finish(error_reason)
    # 
    # def return_bad_request(self, error_code, params=None):
    #     self.return_error(400, error_code, params)
    # 
    # def return_unauthorized(self, error_code, params=None):
    #     self.return_error(401, error_code, params)
    # 
    # def return_forbidden(self, error_code, params=None):
    #     self.return_error(403, error_code, params)
    # 
    # def return_not_found(self, error_code, params=None):
    #     self.return_error(404, error_code, params)
    # 
    # def return_conflict(self, error_code, params=None):
    #     self.return_error(409, error_code, params)
    # 
    # def return_payload_too_large(self, error_code, params=None):
    #     self.return_error(413, error_code, params)
    # 
    # def return_unsupported_media_type(self, error_code, params=None):
    #     self.return_error(415, error_code, params)
    # 
    # def return_unprocessable_entity(self, error_code, params=None):
    #     self.return_error(422, error_code, params)
    # 
    # def return_internal_error(self, error_code, params=None):   # pragma: no cover
    #     self.return_error(500, error_code, params)
