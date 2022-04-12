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

class ProductDto:
    api = Namespace('product', description='product related operations')
    product = api.model('product', {
        'name' : fields.String(required=True, description='The product name'),
        'description' : fields.String(required=True, description='The product description'),
        'price' : fields.String(required=True, description='The product price'),
        'product_id': fields.String(description='The product id')
    })
class CartDto:
    api = Namespace('cart', description='cart related operations')
    cart = api.model('cart', {
        'quantity' : fields.String(description='The cart quantity'),
        'product_id' : fields.String(description='The product id'),
    })
class CartItemDto:
    api = Namespace('cartitem', description='cart item related operations')
    cartItem = api.model('cartitem', {
        'quantity' : fields.String(description='The cart item quantity'),
    })
class OrderDto:
    api = Namespace('order', description='order related operations')
    order = api.model('order', {
        'cart_id' : fields.String(description='The id of cart'),
        'order_id' : fields.String(description='The id of order_id'),
        'payment_status' : fields.String(description='The payment status of order'),
    })