from flask import request
from flask_restx import Resource

from ..util.decorator import token_required
from ..util.dto import CartDto
from ..service.cart_service import save_new_cart,checkout

api = CartDto.api
_cart = CartDto.cart


@api.route('/add')
class Cart(Resource):
    @api.expect(_cart, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('create a new cart')
    @token_required
    def post(self, current_user):
        """Creates a new Cart """
        data = request.json
        return save_new_cart(data=data, customer=current_user)


@api.route('/checkout')
class CartCheckout(Resource):
    @api.response(201, 'Checkout cart successfully created.')
    @api.doc('Checkout cart')
    @token_required
    def post(self, current_user):
        """Checkout Cart"""
        return checkout(user=current_user)