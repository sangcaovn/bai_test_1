from functools import wraps

from flask import request

from app.main.service.auth_helper import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        print ("token>>>",data)
        token = data.get('data')

        print ()
        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated
