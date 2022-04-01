import datetime

from app.main import db
from app.main.model.user import User
from typing import Dict


def save_new_user(data: Dict[str, str]):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(user_uuid):
    return User.query.filter_by(user_uuid=user_uuid).first()


def generate_token(user: User):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.user_uuid)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data: User):
    db.session.add(data)
    db.session.commit()

