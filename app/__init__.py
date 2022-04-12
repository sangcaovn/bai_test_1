from flask_restx import Api
from flask import Blueprint

from .main.controller.auth_controller import api as auth_ctl
from .main.controller.cart_controller import api as cart_ctl
from .main.controller.cart_item_controller import api as cart_item_ctl
from .main.controller.user_controller import api as user_ctl
from .main.controller.product_controller import api as product_ctl
from .main.controller.order_controller import api as order_ctl

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
    title='Order API',
    version='1.0',
    description='Henry Pham assignment 1',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(auth_ctl, path='/auth')
api.add_namespace(user_ctl, path='/user')
api.add_namespace(cart_ctl)
api.add_namespace(cart_item_ctl, path='/cart-item')
api.add_namespace(product_ctl, path='/product')
api.add_namespace(order_ctl, path='/order')
