from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
    })

class CartDto:
    api = Namespace('cart', description='cart related operations')
    cart = api.model('cart', {
        'product_id': fields.String(required=True, description='item id'),
        'item_quantity': fields.Integer(required=True, description='item quantity'),
        # 'product_id': fields.Integer(required=True, description='item id'),
        # 'quantity': fields.Integer(required=True, description='item quantity'),
    })
class ProductDto:
    api = Namespace('product', description='product related operations')
    product = api.model('product', {
        'name': fields.String(required=True, description='product name'),
        'price': fields.Integer(required=True, description='product price'),
    })

class OrderDto:
    api = Namespace('order', description='order related operations')
    order = api.model('order', {
        'order_cart': fields.Integer(required=True, description='order cart'),
        'description': fields.String(required=False, description='order description'),
    })
class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
