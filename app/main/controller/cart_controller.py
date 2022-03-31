from flask import request
from flask_restx import Resource
from app.main.service.cart_service import add_new_cart, checkout_cart

from app.main.util.decorator import admin_token_required
from ..util.dto import CartDto
from typing import Dict


api = CartDto.api
_cart = CartDto.cart

@api.route('/add')
class Cart(Resource):
    @api.doc('list_of_all_carts')
    # @admin_token_required
    @api.expect(_cart, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('create a new cart')
    @admin_token_required
    def post(self):
        """Creates a new Cart """
        data = request.json
        return add_new_cart(data=data)


@api.route('/checkout')
class CartCheckout(Resource):
    @api.doc('checkout_a_card')
    # @admin_token_required
    @api.response(201, 'Cart successfully checkout.')
    @api.doc('checkout a cart')
    @admin_token_required
    def post(self):
        """Checkout a Cart """
        data = request.json
        return checkout_cart(data=data)