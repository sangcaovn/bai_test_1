from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.cart_controller import api as cart_ns
from .main.controller.product_controller import api as product_ns


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
    title='TEST',
    version='1.0',
    description='Le Khanh Duy',
    authorizations=authorizations,
    security='apikey'
)

# api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(cart_ns, path='/cart')
# api.add_namespace(product_ns, path='/product')
