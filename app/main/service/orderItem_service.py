import json
import uuid
from typing import Dict

from app.main import db
from app.main.model.cartItem import CartItem
from app.main.model.orderItem import OrderItem
from .cartItem_service import get_cart_item_list, formatCartItem, delete_cart_item

def create_order_item_list (cart_id, order_id):
    cartitems = get_cart_item_list(cart_id)
    cartItems_result = formatCartItem(cartitems)
    orderitems = []
    for cartitem in cartItems_result:
        new_orderItem = OrderItem(
            orderItem_id=str(uuid.uuid4()),
            order_id=order_id,
            product_id=cartitem['product_id'],
            quantity=cartitem['quantity'],
            subtotal_ex_tax=cartitem['subtotal_ex_tax'],
            tax_total=cartitem['tax_total'],
            total=cartitem['total']
        )
        save_changes(new_orderItem)
        orderitems.append({
            "orderItem_id" : new_orderItem.orderItem_id,
            "order_id" : new_orderItem.order_id,
            "quantity" : new_orderItem.quantity,
            "product_id" : new_orderItem.product_id,
            "subtotal_ex_tax" : new_orderItem.subtotal_ex_tax,
            "tax_total" : new_orderItem.tax_total,
            "total" : new_orderItem.total
        })
        delete_cart_item(cartitem['cartItem_id'])
    return orderitems
def save_changes(data: OrderItem):
    db.session.add(data)
    db.session.commit()