from functools import wraps

from flask import request

from app.main.service.auth_helper import Auth
from typing import Callable


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user_1(request)

        if isinstance(data, str) and status != 200:
            return data, status

        kwargs["current_user"] = data
        return f(*args, **kwargs)

    return decorated


def admin_token_required(f: Callable):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
