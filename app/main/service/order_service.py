
from app.main import db
from app.main.model.order import Order
from typing import Dict


def save_new_order(data: Dict[str, str]):
    order = Order.query.filter_by(order_cart=data['order_cart']).first()
    if not order:
        new_order = Order(
            order_cart=data['order_cart'],
            description=data['description']
        )
        save_changes(new_order)
        return "ok!", 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Order already exists. Please Log in.',
        }
        return response_object, 409


def get_all_orders():
    return Order.query.all()


def get_a_order(id):
    return Order.query.filter_by(id=id).first()


def save_changes(data: Order):
    db.session.add(data)
    db.session.commit()

