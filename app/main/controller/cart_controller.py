from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import CartDto
from ..service.cart_service import add_item_to_cart, save_new_cart
from ..service.cart_item_service import save_new_item
from typing import Dict, Tuple

api = CartDto.api
_cart = CartDto.cart

@api.route('/add/<user_id>')
@api.param('user_id', 'The User identifier')
@api.response(404, 'User not found.')
class Cart(Resource):
    @api.doc('create new cart for a user with user id')
    @api.response(201, 'Cart successfully created.')
    def post(self, user_id):
        """get a user given its identifier"""
        return save_new_cart(user_id)

@api.route('/add-item/<cart_id>')
@api.param('cart_id', 'The Cart identifier')
@api.response(404, 'Cart not found.')
class CartItem(Resource):
    @api.doc('Add item to cart')
    @api.response(201, 'Add item successfully created.')
    @api.expect(_cart, validate=True)
    def post(self, cart_id):
        """ Update items in cart """
        data = request.json
        return save_new_item(cart_id, data=data)