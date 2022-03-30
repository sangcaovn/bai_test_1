
from app.main import db
from app.main.model.cart import Cart
from typing import Dict


def save_new_cart(data: Dict[str, str]):
    cart = Cart.query.filter_by(id=data['id']).first()
    if not cart:
        new_cart = Cart(
            id=data['id'],
            item_quantity=data['item_quantity']
        )
        save_changes(new_cart)
        return new_cart
    else:
        response_object = {
            'status': 'fail',
            'message': 'Cart already exists. Please Log in.',
        }
        return response_object, 409


def get_all_carts():
    return Cart.query.all()


def get_a_cart(id):
    return Cart.query.filter_by(id=id).first()


def save_changes(data: Cart):
    db.session.add(data)
    db.session.commit()

