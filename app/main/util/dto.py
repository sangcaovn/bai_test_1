from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'user_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class CartDto:
    api = Namespace('cart', description='cart related operations')
    cart = api.model('Cart', {
            'productID': fields.String,
            'quantity': fields.Integer
    })

   
class CartItemQuantityDto:
    api = Namespace('cart-item', description='cart item related operations')
    quantity_updater = api.model('CartItemUpdate', {
        'quantity': fields.Integer(required=True, description='The new quantity to update '),
    })
