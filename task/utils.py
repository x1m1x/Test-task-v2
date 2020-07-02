from rest_framework.views import exception_handler

from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response.status_code == 404:
        response = Response(data=";fj;las")
    return response 
