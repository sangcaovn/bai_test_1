from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import CartItemQuantityDto
from ..service.cart_item_service import add_new_item, update_quantity, delete_cart_item
from typing import Dict, Tuple

api=CartItemQuantityDto.api
_cart_item_updater = CartItemQuantityDto.quantity_updater

@api.route('/<cart_item_id>/changeqty')
@api.param('cart_item_id', 'The Cart Item identifier')
@api.response(404, 'Cart Item not found.')
class CartItem(Resource):
    @api.doc('Change quantity in cart item')
    @api.response(200, 'Cart updated successfully.')
    @api.expect(_cart_item_updater, validate=True)
    @token_required
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
    @token_required
    def delete(self, cart_item_id):
        """get a user given its identifier"""
        return delete_cart_item(cart_item_id)