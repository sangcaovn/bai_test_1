from flask import request
from flask_restx import Resource

from app.main.service.order_service import change_order_status
from ..util.dto import OrderDto

api = OrderDto.api
_order = OrderDto.order


@api.route('/')
class Order(Resource):
    @api.expect(_order, validate=True)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request',
        403: 'Forbidden'
    })
    @api.doc('change order status')
    def post(self):
        """Updata order status"""
        data = request.json
        return change_order_status(data)
