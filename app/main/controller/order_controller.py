from typing import Dict, Tuple

from flask import request
from flask_restx import Resource

from ..util.dto import OrderDto
from ..service.order_service import update_a_order

api = OrderDto.api
_order = OrderDto.order

@api.route('/<order_id>')
@api.param('order_id', 'The order_id of order')
@api.response(404, 'Order not found.')
class Ordert(Resource):
    @api.doc('update a order')
    def patch(self, order_id):
        """Update a order """
        data = request.json
        return update_a_order(order_id, data=data)   