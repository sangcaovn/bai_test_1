from flask import request
from flask_restx import Resource
from app.main.service.cart_service import add_new_cart

from app.main.util.decorator import admin_token_required
from ..util.dto import CartDto
from ..service.product_service import add_new_product, get_all_products, get_a_product, update_a_product
from typing import Dict

api = CartDto.api
_cart = CartDto.cart

@api.route('/add')
class Cart(Resource):
    @api.doc('list_of_all_products')
    # @admin_token_required
    @api.expect(_cart, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('create a new cart')
    @admin_token_required
    def post(self):
        """Creates a new Cart """
        data = request.json
        return add_new_cart(data=data)