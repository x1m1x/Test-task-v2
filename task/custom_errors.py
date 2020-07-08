import json

from rest_framework import status

from django.http import HttpResponseNotFound, HttpResponse


def error500(request):
    response_data = {}
    response_data['detail'] = 'Server error'
    return HttpResponse(json.dumps(response_data), content_type="application/json", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def error400(request, exception):
    response_data = {}
    response_data['detail'] = 'Bad request'
    return HttpResponse(json.dumps(response_data), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

def error403(request, exception):
    response_data = {}
    response_data['detail'] = 'Forbidden'
    return HttpResponse(json.dumps(response_data), content_type="application/json", status=status.HTTP_403_FORBIDDEN)

def error404(request, exception):
    response_data = {}
    response_data['detail'] = 'Not found'
    return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")
