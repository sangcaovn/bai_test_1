
from ast import Dict
from app.main import db

from app.main.model.cart import Cart
from typing import Dict


def save_new_cart(data: Dict[str, str]):
    new_cart = Cart(
        product_id=data['productId'],
        quantity=data['quantity'],
    )
    return save_changes(new_cart)


def save_changes(data: Cart):
    db.session.add(data)
    db.session.commit()
