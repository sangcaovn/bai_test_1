from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user data to create new')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password')
    })


class CartDto:
    api = Namespace('cart', description='post new cart')
    cart = api.model('cart', {
        'productId': fields.String(required=True, description='productId'),
        'quantity': fields.Integer(required=True, description='quantity'),
    })

class CartItemDto:
    api = Namespace('cart_item', description='cart item string data to update,delete')
    cart_item_id = api.model('cart_item_change_qty', {
        'quantity': fields.String(required=True, description='quantity')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
