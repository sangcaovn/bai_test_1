from app.main import db
from flask import request

from app.main.model.cart import Cart
import datetime
from typing import Dict

from app.main.model.cart_item import CartItem
from app.main.model.order import Order
from app.main.model.order_detail import OrderDetail
from app.main.model.user import User
from app.main.service.auth_helper import Auth
from app.main.service.cart_item_service import save_new_item
from app.main.service.order_detail_service import save_new_order_detail
from app.main.service.order_service import save_new_order

def get_cart(cart_id: int):
    return Cart.query.filter_by(id=cart_id).first()


def save_changes(cart: Cart):
    db.session.add(cart)
    db.session.commit()


def update_cart(cart_id: id, cart_items):
    num_rows_updated = Cart.query.filter_by(id=cart_id).update(dict(cart_items=cart_items))
    db.session.commit()

    return num_rows_updated


def add_cart(data):
    user_id = Auth.get_cart_from_user_id(request)
    cart = Cart.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(id=user_id).first()
    if not cart:
        # Create a new cart
        new_cart = Cart(
            create_at=datetime.datetime.utcnow(),
            update_at=datetime.datetime.utcnow(),
            user_id = user_id
        )
        save_changes(new_cart)
        # Re-query to get cart
        cart = Cart.query.filter_by(user_id=user_id).first()
        cart_id = cart.id
        cart_uuid = cart.cart_uuid
        # save cart item
        return save_new_item(user.public_id, cart_uuid, cart_id=cart_id, data=data)
    else:
        return save_new_item(user.public_id, cart.cart_uuid, cart_id=cart.id, data=data)


def checkout():
    user_id = Auth.get_cart_from_user_id(request)
    user = User.query.filter_by(id=user_id).first()
    cart = Cart.query.filter_by(user_id = user_id).first()
    cart_id = cart.id
    cart_items = CartItem.query.filter_by(cart_id = cart_id).all()

    # Create new order
    order_id = save_new_order(user_id)
    # Create order details
    for item in cart_items:
        save_new_order_detail(order_id, item)

    # Remove cart items
    for item in cart_items:
        CartItem.query.filter_by(id=item.id).delete()
        db.session.commit()

    # Re-query to get payment status
    order = Order.query.filter_by(id = order_id).first()
    order_details = OrderDetail.query.filter_by(order_id=order_id).all()
    # cart_items_json_string = json.dumps([ob for ob in cart_items])
    order_detail_items_list_json = []
    order_subtotal_ex_tax = 0
    order_tax_total = 0
    order_total = 0

    for detail in order_details:
        info = {}
        info['order_item_id'] = detail.id
        info['product_id'] = detail.product_id
        info['quantity'] = detail.quantity
        info['subtotal_ex_tax'] = detail.subtotal_ex_tax
        info['tax_total'] = detail.tax_total
        info['total'] = detail.total
        order_detail_items_list_json.append(info)
        order_subtotal_ex_tax += detail.subtotal_ex_tax
        order_tax_total += detail.tax_total
        order_total += detail.total

    response_object = {
            "order_id": f"{order.order_uuid}",
            "user_id": f"{user.public_id}",
            "cart_items": order_detail_items_list_json,
            "subtotal_ex_tax": order_subtotal_ex_tax,
            "tax_total": order_tax_total,
            "total": order_total,
            "payment_status": f"{order.payment_status}"
        }

    return response_object, 200