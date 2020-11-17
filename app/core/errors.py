from flask import jsonify
from flask_api import status as status_codes


class ServiceException(Exception):
    """Base service exception class"""

    status_code = status_codes.HTTP_500_INTERNAL_SERVER_ERROR
    message = "INTERNAL SERVER ERROR"
    error_code = 'INTERNAL_SERVER_ERROR'

    def __init__(self, message=None, errors=None, status_code=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code

        self.payload = {
            "message": self.message
        }

        if errors:
            self.payload["errors"] = errors
        if self.error_code:
            self.payload["error_code"] = self.error_code
        super().__init__(self.message)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class BadRequestException(ServiceException):
    status_code = status_codes.HTTP_400_BAD_REQUEST
    message = "Bad Request"
    error_code = 'BAD_REQUEST'


class ValidationError(ServiceException):
    status_code = status_codes.HTTP_400_BAD_REQUEST
    message = "Validation Error"
    error_code = 'VALIDATION_ERROR'


def handle_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
