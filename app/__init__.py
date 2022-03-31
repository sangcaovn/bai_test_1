from flask_restx import Api
from flask import Blueprint

from .main.controller.auth_controller import api as auth_ctl
from .main.controller.cart_controller import api as cart_ctl
from .main.controller.cart_item_controller import api as cart_item_ctl

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='FLASK RESTPLUS(RESTX) API WITH JWT',
    version='1.0',
    description='A flask restplus (restx) web service',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(auth_ctl, path='/user')
api.add_namespace(cart_ctl)
api.add_namespace(cart_item_ctl, path='/cart-item')
