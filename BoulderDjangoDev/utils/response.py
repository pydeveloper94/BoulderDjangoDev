"""This module contains all http return messages for json responses."""

from django.http import HttpResponse
from .errors import InvalidJSONResponse
import json

def _HttpMessage(message, status):
    if (message == None) and (status < 400):
        message = {"code": status}
    if (status > 399) and ("errors" not in message):
        message = {"errors": message}
    try:
        message = json.dumps(message)
    except Exception:
        print(message)
        raise InvalidJSONResponse("You have attempted to return a json "
            "response with a non-serializable object. Please look at the "
            "previous print statement for help.")
    return HttpResponse(message, status=status,
        content_type='application/json')

def Http200(message=None):
    return _HttpMessage(message, 200)

def Http201(message=None):
    return _HttpMessage(message, 201) 

def Http400(message=None):
    return _HttpMessage(message, 400)

def Http403(message=None):
    return _HttpMessage(message, 403)

def Http404(message=None):
    return _HttpMessage(message, 404)

def Http500(message=None):
    return _HttpMessage(message, 500)
