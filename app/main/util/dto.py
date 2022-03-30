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
    cart_item_fields = api.model('CartItem', {
    # 'id': fields.String,
    'product_id': fields.String,
    'quantity': fields.Integer
})

    cart = api.model('Cart', {
        # 'create_at': fields.DateTime(required=True, description="Time cart created"),
        # 'update_at': fields.DateTime(required=True, description="Time cart updated"),
        'cart_id': fields.Integer(description="cart identifier"),
        'user_id': fields.Integer(description="user identifier"),
        'cart_items': fields.List(fields.Nested(cart_item_fields), description = "cart items")
    })
