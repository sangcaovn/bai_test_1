from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required

from ..util.dto import CartItemDto
from ..service.cart_service import change_cart_quantity, delete_cart_item

api = CartItemDto.api
_cart_item = CartItemDto.cart_item_id


@api.route('/<cart_item_id>')
@api.param('cart_item_id', 'The cart item id using to get cart item')
class CartItem(Resource):
    @api.response(201, 'delete cart item successfully.')
    @api.doc('delete cart item cart item')
    @token_required
    def delete(self,cart_item_id):
        return delete_cart_item(cart_item_id)


@api.route('/<cart_item_id>/changeqty')
@api.param('cart_item_id', 'The cart item id using to get cart item')
class CartItem(Resource):
    @api.expect(_cart_item, validate=True)
    @api.response(201, 'update quantity cart item successfully.')
    @api.doc('change quantity of cart item')
    @token_required
    def put(self,cart_item_id):
        data = request.json
        return change_cart_quantity(cart_item_id,data=data)

