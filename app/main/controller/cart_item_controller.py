from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import CartDto, CartItemDtoQuantity
from ..service.cart_item_service import save_new_item, update_quantity, delete_cart_item
from typing import Dict, Tuple

api = CartDto.api
_cart = CartDto.cart

_cart_item_updater = CartItemDtoQuantity.api

@api.route('/add-item/<cart_id>')
@api.param('cart_id', 'The Cart identifier')
@api.response(404, 'Cart not found.')
class CartItemCreator(Resource):
    @api.doc('Add item to cart')
    @api.response(201, 'Add item successfully created.')
    @api.expect(_cart, validate=True)
    def post(self, cart_id):
        """ Update items in cart """
        data = request.json
        return save_new_item(cart_id, data=data)

@api.route('/<cart_item_id>/changeqty')
@api.param('cart_item_id', 'The Cart Item identifier')
@api.response(404, 'Cart Item not found.')
class CartItem(Resource):
    @api.doc('Change quantity in cart item')
    @api.response(200, 'Cart updated successfully.')
    @api.expect(_cart_item_updater, validate=True)
    def put(self, cart_item_id):
        """get a user given its identifier"""
        data = request.json
        return update_quantity(cart_item_id, data = data)

@api.route('/<cart_item_id>')
@api.param('cart_item_id', 'The Cart Item identifier')
@api.response(404, 'Cart Item not found.')
class CartItemRemover(Resource):
    @api.doc('Remove the cart item')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(403, 'Forbidden')
    def delete(self, cart_item_id):
        """get a user given its identifier"""
        return delete_cart_item(cart_item_id)