from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user data to create new')
    user = api.model('user', {
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password')
    })


class CartDto:
    api = Namespace('cart', description='post new cart')
    cart = api.model('cart', {
        'product_id': fields.String(required=True, description='productId'),
        'quantity': fields.Integer(required=True, description='quantity'),
    })


class CartItemDto:
    api = Namespace('cart_item', description='cart item string data to update,delete')
    cart_item_id = api.model('cart_item_change_qty', {
        'quantity': fields.Integer(required=True, description='quantity')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'username': fields.String(required=True, description='The username address'),
        'password': fields.String(required=True, description='The user password '),
    })


class ProductDto:
    api = Namespace('product', description='product related operations')
    product = api.model('product', {
        'name': fields.String(required=True, description='The product name'),
        'price': fields.String(required=True, description='The product price'),
    })


class OrderDto:
    api = Namespace('order', description='order related operations')
    order = api.model('order', {
        'order_id': fields.String(required=True, description='The product name'),
        'payment_status': fields.String(required=True, description='The product price'),
    })
