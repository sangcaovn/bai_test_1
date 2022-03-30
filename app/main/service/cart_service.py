import json
import uuid
from typing import Dict

from app.main import db
from app.main.model.cart import Cart
from .cartItem_service import create_a_cart_item


def create_a_cart(user_id, data: Dict[str, str]):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        new_cart = Cart(
            cart_id=str(uuid.uuid4()),
            user_id=user_id,
            quantity=int(data['quantity'])
        )
        save_changes(new_cart)

        data_cartitem = create_a_cart_item(new_cart.cart_id, data)

        print(data_cartitem[0][data])

        response_object = {
            'status': 'success',
            'message': 'Successfully created.',
            'data': {
                "cart_id": new_cart.cart_id,
                "quantity": new_cart.quantity,
                "user_id": new_cart.user_id
            }
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Cart already exists.',
        }
        return response_object, 409


def checkout(cart_id: str):
    cart = Cart.query.filter_by(cart_id=cart_id)
    order = Order



def save_changes(data: Cart):
    db.session.add(data)
    db.session.commit()
