from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.product_controller import api as product_ns
from .main.controller.cart_controller import api as cart_ns
from .main.controller.cartItem_controller import api as cartItem_ns
from .main.controller.order_controller import api as order_ns
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
    title='DANG NGUYRN HOAI THU - TEST 01',
    version='1.0',
    description='API written by Dang Nguyen Hoai Thu',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(product_ns)
api.add_namespace(cart_ns)
api.add_namespace(cartItem_ns)
api.add_namespace(order_ns)