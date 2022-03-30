import json
from app.main import db
from flask import jsonify
from app.main.model.cart import Cart
import datetime
from typing import Dict

from app.main.model.cart_item import CartItem

def save_new_cart(user_id : int):
    cart = Cart.query.filter_by(user_id=user_id).first()
    response_object = {}
    if not cart:
        new_cart = Cart(
            create_at=datetime.datetime.utcnow(),
            update_at=datetime.datetime.utcnow(),
            user_id = user_id
        )
        save_changes(new_cart)
        response_object = {
            "status": "success!",
            "message": f"Create cart for user whose id = {user_id} successfully!"
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': f'Cart for this user whose id = {user_id} has already exists. Please Log in.',
        }
        return response_object, 409

def get_cart(cart_id: int):
    return Cart.query.filter_by(id=cart_id).first()

def add_item_to_cart(cart_id: int, data: Dict[str, str]):
    cart = get_cart(cart_id)
    cart_items = list(cart.cart_items)

    cart_items.append(data)
    # cart.cart_items = cart_items
    # Update cart
    # num_rows_updated = update_cart(cart_id, cart_items)
    response_object = {
            "status": "success!",
            "message": f"Update item to car  whose id = {cart_id} successfully! Type cart: {type(cart_items)}. {(cart_items[0])}"
        }
    return response_object, 200

def save_changes(cart: Cart):
    db.session.add(cart)
    db.session.commit()

def update_cart(cart_id: id, cart_items):
    num_rows_updated = Cart.query.filter_by(id=cart_id).update(dict(cart_items=cart_items))
    db.session.commit()

    return num_rows_updated
