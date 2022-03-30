from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import CartDto
from ..service.cart_service import save_new_cart, get_all_carts, get_a_cart
from typing import Dict, Tuple

api = CartDto.api
_cart = CartDto.cart


@api.route('/')
class CartList(Resource):
    @api.doc('list_of_carts')
    @admin_token_required
    @api.marshal_list_with(_cart, envelope='data')
    def get(self):
        """List all registered carts"""
        return get_all_carts()

    @api.expect(_cart, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('create a new cart')
    def post(self):
        """Creates a new Cart """
        data = request.json
        return save_new_cart(data=data)


@api.route('/<id>')
@api.param('id', 'The Cart identifier')
@api.response(404, 'Cart not found.')
class Cart(Resource):
    @api.doc('get a cart')
    @api.marshal_with(_cart)
    def get(self, id):
        """get a cart given its identifier"""
        cart = get_a_cart(id)
        if not cart:
            api.abort(404)
        else:
            return cart

