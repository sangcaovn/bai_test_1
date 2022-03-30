from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import OrderDto
from ..service.order_service import save_new_order, get_all_orders, get_a_order
from typing import Dict, Tuple

api = OrderDto.api
_order = OrderDto.order


@api.route('/')
class OrderList(Resource):
    @api.doc('list_of_orders')
    @admin_token_required
    @api.marshal_list_with(_order, envelope='data')
    def get(self):
        """List all registered orders"""
        return get_all_orders()

    @api.expect(_order, validate=True)
    @api.response(201, 'Order successfully created.')
    @api.doc('create a new order')
    def post(self):
        """Creates a new Order """
        data = request.json
        return save_new_order(data=data)


@api.route('/<order_id>')
@api.param('id', 'The Order identifier')
@api.response(404, 'Order not found.')
class Order(Resource):
    @api.doc('get a order')
    @api.marshal_with(_order)
    def get(self, id):
        """get a order given its identifier"""
        order = get_a_order(id)
        if not order:
            api.abort(404)
        else:
            return order

