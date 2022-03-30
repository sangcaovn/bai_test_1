from flask import request
from flask_restx import Resource

from app.main.service.auth_helper import Auth
from app.main.util.decorator import token_required
from ..service.cart_service import create_a_cart, checkout
from ..util.dto import CartDto

api = CartDto.api
_cart = CartDto.cart
_cart_checkout = CartDto.cart_checkout


@api.route('/')
class Cart(Resource):
    @api.expect(_cart, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('create a cart')
    @token_required
    def post(self):
        """Creates a cart """
        data = request.json
        auth_data, status = Auth.get_logged_in_user(request)
        token = auth_data.get('data')
        user_id = token.get('user_id')
        return create_a_cart(user_id, data=data)


@api.route("/checkout")
class CartCheckout(Resource):
    @api.expect(_cart_checkout, validate=True)
    @api.response(200, "")
    @token_required
    def post(self):
        data = request.json
        return checkout(cart_id=data.get("cart_id"))
