from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required
from ..util.dto import CartDto
from ..service.cart_service import add_cart, checkout


api = CartDto.api
_cart = CartDto.cart

@api.route('/add')
class Cart(Resource):
    @api.doc('add product to cart')
    @api.response(404, 'User not found.')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(403, 'Forbidden')
    @api.expect(_cart, validate = True)
    @token_required
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
    @token_required
    def post(self):
        """get a user given its identifier"""
        return checkout()