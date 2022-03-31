from app.main import db
from flask import request
from app.main.enum.type_enum import TypeEnum
from app.main.model.cart import Cart
import datetime
from typing import Dict

from app.main.model.cart_item import CartItem
from app.main.model.user import User
from app.main.service.auth_helper import Auth
from app.main.service.cart_item_service import change_type_after_checking_out, save_new_item

def get_cart(cart_id: int):
    return Cart.query.filter_by(id=cart_id).first()

def save_changes(cart: Cart):
    db.session.add(cart)
    db.session.commit()

def update_cart(cart_id: id, cart_items):
    num_rows_updated = Cart.query.filter_by(id=cart_id).update(dict(cart_items=cart_items))
    db.session.commit()

    return num_rows_updated

def change_type_cart_after_checking_out(cart_id:int):
    num_rows_updated = Cart.query.filter_by(id=cart_id).update(dict(type=TypeEnum.Order.value))
    db.session.commit()

    return num_rows_updated

def change_payment_status_after_checking_out(cart_id:int):
    num_rows_updated = Cart.query.filter_by(id=cart_id).update(dict(payment_status='INIT'))
    db.session.commit()

    return num_rows_updated

def add_cart(data):
    user_id = Auth.get_cart_from_user_id(request)
    cart = Cart.query.filter_by(user_id=user_id).first()
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
        return save_new_item(user_id, cart_uuid, cart_id=cart_id, data=data)
    else:
        return save_new_item(user_id, cart.cart_uuid, cart_id=cart.id, data=data)


def checkout():
    user_id = Auth.get_cart_from_user_id(request)
    user = User.query.filter_by(id=user_id).first()
    cart = Cart.query.filter_by(user_id = user_id).first()
    cart_id = cart.id

    # Change type from cart to order
    num_row_updated = change_type_cart_after_checking_out(cart_id)
    # Change payment_status to INIT
    num_row_updated = change_payment_status_after_checking_out(cart_id)
    # Change type of cart items to order details
    num_row_updated = change_type_after_checking_out(cart_id)

    # Re-query to get payment status
    cart = Cart.query.filter_by(user_id = user_id).first()
    cart_items = CartItem.query.filter_by(cart_id=cart_id).all()
    # cart_items_json_string = json.dumps([ob for ob in cart_items])
    cart_items_list_json = []
    cart_subtotal_ex_tax = 0
    cart_tax_total = 0
    cart_total = 0

    for item in cart_items:
        info = {}
        info['order_item_id'] = item.id
        info['product_id'] = item.product_id
        info['quantity'] = item.quantity
        info['subtotal_ex_tax'] = item.subtotal_ex_tax
        info['tax_total'] = item.tax_total
        info['total'] = item.total
        cart_items_list_json.append(info)
        cart_subtotal_ex_tax += item.subtotal_ex_tax
        cart_tax_total += item.tax_total
        cart_total += item.total

    response_object = {
            "order_id": f"{cart.cart_uuid}",
            "user_id": f"{user.public_id}",
            "cart_items": cart_items_list_json,
            "subtotal_ex_tax": cart_subtotal_ex_tax,
            "tax_total": cart_tax_total,
            "total": cart_total,
            "payment_status": f"{cart.payment_status}"
        }

    return response_object, 200