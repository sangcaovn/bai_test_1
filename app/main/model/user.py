from datetime import datetime, timedelta

import jwt

from app.main.model.blacklist import BlacklistToken
from .. import db, flask_bcrypt
from .. import generate_uuid
from ..config import key


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    create_at = db.Column(db.DateTime, default=datetime.now())

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id: str):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token: str):
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)
