from typing import Dict, Tuple

from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required
from ..util.dto import CartItemDto
from ..service.cartItem_service import update_a_cart_item, delete_cart_item


api = CartItemDto.api
_cart = CartItemDto.cartItem

@api.route('/<cartItem_id>/changeqty')
@api.param('cartItem_id', 'The quantity of cart item')
@api.response(404, 'Cart item not found.')
class CartItem(Resource):
    @api.doc('update a cart item')
    @token_required
    def patch(self, cartItem_id):
        """Update a quantity of cart item """
        data = request.json
        return update_a_cart_item(cartItem_id, data)
@api.route('/<cartItem_id>')
@api.param('cartItem_id', 'The quantity of cart item')
@api.response(404, 'Cart item not found.')
class CartItemList(Resource):
    @api.doc('update a cart item')
    @token_required
    def delete(self, cartItem_id):
        """Delete a quantity of cart item """
        return delete_cart_item(cartItem_id)
