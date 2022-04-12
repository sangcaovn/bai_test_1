import json
import uuid
from typing import Dict

from app.main import db
from app.main.model.cart import Cart
from app.main.model.cartItem import CartItem
from app.main.model.order import Order

from .orderItem_service import create_order_item_list
def create_a_order(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
            response_object = {
                'status': 'fail',
                'message': 'Cart doesn\'t exists.',
                }
            return response_object, 404
    new_order = Order(
        order_id=str(uuid.uuid4()),
        user_id=user_id,
        quantity=cart.quantity,
        subtotal_ex_tax=cart.subtotal_ex_tax,
        tax_total=cart.tax_total,
        total=cart.total
    )
    save_changes(new_order)
    orderitems = create_order_item_list(cart.cart_id, new_order.order_id)

    response_object = {
        'status': 'success',
        'message': 'Successfully created.',
        'data': {
            "order_id" : new_order.order_id,
            "quantity" : new_order.quantity,
            "user_id" : new_order.user_id,
            "order_items" : orderitems,
            "subtotal_ex_tax" : new_order.subtotal_ex_tax,
            "tax_total" : new_order.tax_total,
            "total" : new_order.total,
            "payment_status" : new_order.payment_status
        } 
    }
    return response_object, 201
def update_a_order(order_id, data: Dict[str, str]):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        response_object = {
            'status': 'fail',
            'message': 'Order not exists.',
        }
        return response_object, 404
    order.payment_status = data['payment_status']
    save_changes(order)
    response_object = {
            'status': 'success',
            'message': 'Successfully updated',
            'data': {
                "order_id" : order.order_id,
                "quantity" : order.quantity,
                "user_id" : order.user_id,
                "subtotal_ex_tax" : order.subtotal_ex_tax,
                "tax_total" : order.tax_total,
                "total" : order.total,
                "payment_status" : order.payment_status
            }
    }
    return response_object, 200
def get_a_order(order_id):
    return Order.query.filter_by(order_id =order_id).first()
def save_changes(data: Order):
    db.session.add(data)
    db.session.commit()
