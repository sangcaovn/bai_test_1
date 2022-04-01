from app.main.model.order import Order
import datetime
import uuid
from app.main import db
from app.main.model.order_detail import OrderDetail


def save_new_order_detail(order_id, cart_item):
    new_order_detail_uuid = str(uuid.uuid4())
    order_detail = OrderDetail(
        id = new_order_detail_uuid,
        product_id = cart_item.product_id,
        quantity = cart_item.quantity,
        subtotal_ex_tax = cart_item.subtotal_ex_tax,
        tax_total = cart_item.tax_total,
        total = cart_item.total,
        order_id=order_id
    )
    save_changes(order_detail)
    

def save_changes(order_detail: OrderDetail):
    db.session.add(order_detail)
    db.session.commit()