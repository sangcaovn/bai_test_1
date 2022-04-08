from app.main.controller.cart_item_controller import CartItem
from app.main.model.cart import Cart
from app.main.model.order import Order
import datetime
import uuid
from flask import request
from app.main import db
from app.main.service.auth_helper import Auth
from app.main.service.order_detail_service import save_new_order_detail


def save_new_order(user_id):
    new_order_uuid = str(uuid.uuid4())
    order = Order(
        create_at = datetime.datetime.utcnow(),
        update_at = datetime.datetime.utcnow(),
        order_uuid = new_order_uuid,
        user_id = user_id
    )
    save_changes(order)
    # Re-query to get order ID
    new_order = Order.query.filter_by(order_uuid = new_order_uuid).first()
    order_id = new_order.id

    return order_id
    
def update_order_status(data):
    order_id = data['order_id']
    status = data['status']
    num_rows_updated = Order.query.filter_by(order_uuid=order_id).update(dict(payment_status=status))
    db.session.commit()

    response_object = {
        "order_id": f"{order_id}",
        "status": f"{status}"
    }

    return response_object, 200

def save_changes(order: Order):
    db.session.add(order)
    db.session.commit()