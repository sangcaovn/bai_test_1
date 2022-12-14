from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required

from ..util.dto import CartDto
from ..service.cart_service import save_new_cart,checkout_cart

api = CartDto.api
_cart = CartDto.cart


@api.route('/add')
class Cart(Resource):
    @api.expect(_cart, validate=True)
    @api.doc('create a new cart')
    @token_required
    def post(self):
        """Creates a new Cart """
        data = request.json
        return save_new_cart(data=data)


@api.route('/checkout')
class CartCheckout(Resource):
    @api.doc('Checkout cart')
    @token_required
    def post(self):
        """Checkout Cart"""
        return checkout_cart()