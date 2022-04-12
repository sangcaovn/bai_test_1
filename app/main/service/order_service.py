from app.main import db
from app.main.model import PaymentStatus
from app.main.model.cart import Order


def change_order_status(data):
    order_id = data['order_id']
    payment_status = data['payment_status']
    order = Order.query.filter_by(id=order_id).first()
    if order:
        order.payment_status = PaymentStatus[payment_status].value
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': ' update order status successful.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'order does not exist.',
        }
        return response_object, 400
