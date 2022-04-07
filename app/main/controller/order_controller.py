from flask import request
from flask_restx import Resource
from app.main.service.order_service import update_order_status

from app.main.util.decorator import token_required
from ..util.dto import OrderStatus

api = OrderStatus.api
_order = OrderStatus.order_status_modifier

@api.route('/change-order-status')
class OrderStatusChange(Resource):
    # @api.expect(_order, validate = True)
    def post(self):
        """Change order status"""
        data = request.json
        return update_order_status(data=data)