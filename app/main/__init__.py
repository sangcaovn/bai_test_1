from uuid import uuid4

from flask.app import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def generate_uuid():
    return str(uuid4())


def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
