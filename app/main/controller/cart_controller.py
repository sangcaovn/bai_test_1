from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import CartDto
from ..service.cart_service import del_cart_item, save_new_cart, change_qty, cart_check_out
from typing import Dict, Tuple

api = CartDto.api
_cart = CartDto.cart


@api.route('/')
class CartList(Resource):
    # @admin_token_required
    @api.expect(_cart, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('create a new cart')
    def post(self):
        """Creates a new Cart """
        data = request.json
        return save_new_cart(data=data)


@api.route('/<cart_item_id>')
class CartItem(Resource):
    @api.doc('delete cart item')
    def delete(self, cart_item_id):
        """get a cart given its identifier"""
        data = request.json
        return del_cart_item(cart_item_id)

@api.route('/<cart_item_id>/<quantity>')
class CartItem(Resource):
    @api.doc('change quantity cart item')
    def put(self,cart_item_id, quantity):
        """get a cart given its identifier"""
        data = request.json
        return change_qty(cart_item_id,quantity)

@api.route('/cart_checkout')
class CartCheckout(Resource):
    @api.doc('cart checkout')
    @api.response(201, 'Cart Checkout')
    def post(self):
        """Creates a new Cart """
        data = request.json
        return cart_check_out()