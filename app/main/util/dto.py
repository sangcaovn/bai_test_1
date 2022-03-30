from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        # 'user_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class ProductDto:
    api = Namespace('product', description='product related operations')
    product = api.model('product', {
        'name': fields.String(required=True, description='The product name'),
        'description': fields.String(required=True, description='The product description'),
        'price': fields.String(required=True, description='The product price'),
        'product_id': fields.String(description='product_id Identifier'),
    })

class CartDto:
    api = Namespace('cart', description='cart related operations')
    cart = api.model('cart', {
        'product_id': fields.String(required=True, description='The product id'),
        'quantity': fields.Integer(description='The cart quantity'),
    })