from rest_framework.exceptions import APIException
from .error_message import get_error_message


class CustomApiException(APIException):

    def __init__(self, error_code=None, ok=False):
        error_detail = get_error_message(error_code)
        self.status_code = error_detail['http_status']
        self.detail = {
            'detail': error_detail['result'],
            'ok': ok,
            'result': '',
            'error_code': error_code
        }
