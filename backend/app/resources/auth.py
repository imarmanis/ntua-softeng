from functools import wraps
from flask import request
from werkzeug.http import parse_authorization_header


def check_auth(user):
    return user.username == 'foo' and user.password == 'bar'


def requires_auth(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        user = parse_authorization_header(request.headers.get('X-OBSERVATORY-AUTH'))
        if not (user and check_auth(user)):
            return {'errors': ['Not authorized']}, 403
        return f(*args, **kwargs)
    return decorated
