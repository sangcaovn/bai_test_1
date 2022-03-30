from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'user_id': fields.String(description='user Identifier')
    })

class CartDto:
    api = Namespace('cart', description='cart related operations')
    cart = api.model('cart', {
        'item_id': fields.Integer(required=True, description='item id'),
        'item_quantity': fields.Integer(required=True, description='item quantity'),
    })

class ProductDto:
    api = Namespace('product', description='product related operations')
    product = api.model('product', {
        'product_id': fields.Integer(required=True, description='product id'),
        'name': fields.String(required=True, description='product name'),
        'price': fields.Integer(required=True, description='product price'),
        'description': fields.String(required=False, description='product description'),
    })

class OrderDto:
    api = Namespace('order', description='order related operations')
    order = api.model('order', {
        'order_id': fields.Integer(required=True, description='order id'),
        'order_cart': fields.Integer(required=True, description='order cart'),
        'description': fields.String(required=False, description='order description'),
        'total': fields.Integer(required=True, description='total price'),
    })
class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
