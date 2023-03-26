from flask import request
from flask_restx import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user
from app.main.service.auth_helper import Auth

from app.main.util.decorator import token_required

api = UserDto.api
_user = UserDto.user


@api.route('/')
class User(Resource):
    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


    @api.doc('get a logged in user')
    @token_required
    def get(self):
        """get a user given its identifier"""
        print (request)
        token = request.json
        user = Auth.get_logged_in_user(token)
        if not user:
            api.abort(404)
        else:
            return user