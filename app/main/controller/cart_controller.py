from flask import request
from flask_restx import Resource

from app.main.service.auth_helper import Auth
from app.main.util.decorator import token_required
from ..model.cart import Cart
from ..service.cart_service import create_a_cart, checkout
from ..util.dto import CartDto

api = CartDto.api
_cart = CartDto.cart
_cart_checkout = CartDto.cart_checkout


@api.route('/')
class CartView(Resource):
    @api.expect(_cart, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('create a cart')
    @token_required
    def post(self, current_user):
        """Creates a cart """
        data = request.json
        return create_a_cart(current_user.public_id, data=data)


@api.route("/checkout")
class CartCheckout(Resource):
    @api.expect(_cart_checkout, validate=True)
    @api.response(200, "")
    @token_required
    def post(self, current_user):
        cart = Cart.get_cart_by_user_id(current_user.public_id)
        if not cart:
            return "User does not have any cart", 400
        return checkout(cart)
