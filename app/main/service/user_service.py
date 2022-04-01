from typing import Dict

from app.main import db
from app.main.model.user import User


def save_new_user(data: Dict[str, str]):
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        new_user = User(
            username=data['username'],
            password=data['password']
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


def get_a_user(id):
    return User.query.filter_by(id=id).first()


def generate_token(user: User):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
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
