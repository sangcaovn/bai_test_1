from flask import request
from flask_restx import Resource

from ..util.dto import CartDto
from ..service.cart_service import save_new_cart

api = CartDto.api
_cart = CartDto.cart


@api.route('/add')
class Cart(Resource):
    @api.expect(_cart, validate=True)
    @api.response(201, 'Cart successfully created.')
    @api.doc('create a new cart')
    def post(self):
        """Creates a new Cart """
        data = request.json
        return save_new_cart(data=data)

