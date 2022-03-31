from typing import Dict, Tuple

from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required
from ..util.dto import CartDto
from ..service.cart_service import create_a_cart
from ..service.order_service import create_a_order
from app.main.service.auth_helper import Auth

api = CartDto.api
_cart = CartDto.cart

@api.route('/')
class Cart(Resource):
    @api.expect(_cart, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('create a cart')
    @token_required
    def post(self):
        """Creates a cart """
        data = request.json
        auth_data, status = Auth.get_logged_in_user(request)
        token = auth_data.get('data')
        user_id = token.get('user_id')
        return create_a_cart(user_id,data=data)
@api.route('/checkout')
class CartCheckout(Resource):
    @api.response(201, 'Cart successfully checkout.')
    @api.doc('checkout a cart')
    @token_required
    def post(self):
        """Checkout a cart """
        auth_data, status = Auth.get_logged_in_user(request)
        token = auth_data.get('data')
        user_id = token.get('user_id')
        return create_a_order(user_id)

