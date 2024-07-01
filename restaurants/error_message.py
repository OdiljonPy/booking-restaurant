from rest_framework import status

error_messages = {
    1: {"result": "This action does not acceptable", "http_status": status.HTTP_406_NOT_ACCEPTABLE},
    2: {"result": "Invalid input provided", "http_status": status.HTTP_400_BAD_REQUEST},
    3: {"result": "Unauthorized access", "http_status": status.HTTP_401_UNAUTHORIZED},
    4: {"result": "Resource not found", "http_status": status.HTTP_404_NOT_FOUND},
}


def get_error_message(code):
    return error_messages.get(code, 'Unknown error')
