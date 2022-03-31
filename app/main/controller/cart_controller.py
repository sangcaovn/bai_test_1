from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import CartDto, CartOveralDto
from ..service.cart_service import add_cart, add_item_to_cart, checkout, save_new_cart
from ..service.cart_item_service import save_new_item
from typing import Dict, Tuple

api = CartDto.api
_cart = CartDto.cart

# _cart_overal = CartOveralDto.cart_overal

# @api.route('/add/<user_id>')
# @api.param('user_id', 'The User identifier')
# @api.response(404, 'User not found.')
# class Cart(Resource):
#     @api.doc('create new cart for a user with user id')
#     @api.response(201, 'Cart successfully created.')
#     def post(self, user_id):
#         """get a user given its identifier"""
#         return save_new_cart(user_id)

# @api.route('/add-item/<cart_id>')
# @api.param('cart_id', 'The Cart identifier')
# @api.response(404, 'Cart not found.')
# class CartItem(Resource):
#     @api.doc('Add item to cart')
#     @api.response(201, 'Add item successfully created.')
#     @api.expect(_cart, validate=True)
#     def post(self, cart_id):
#         """ Update items in cart """
#         data = request.json
#         return save_new_item(cart_id, data=data)

@api.route('/add')
class Cart(Resource):
    @api.doc('add product to cart')
    @api.response(404, 'User not found.')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(403, 'Forbidden')
    @api.expect(_cart, validate = True)
    def post(self):
        """create cart for loggin user"""
        data = request.json
        return add_cart(data=data)


@api.route('/checkout')
@api.response(200, 'OK')
@api.response(400, 'Bad Request')
@api.response(403, 'Forbidden')
class CartCheckout(Resource):
    @api.doc('Check the cart out for the current user')
    @api.response(200, 'Cart successfully checked out.')
    def post(self):
        """get a user given its identifier"""
        return checkout()