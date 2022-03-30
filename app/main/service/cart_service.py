import uuid
from flask import request
from app.main import db
from app.main.model.cart import Cart
from typing import Dict
from app.main.service.auth_helper import Auth
from app.main.model.user import User
from app.main.service.cartitem_service import add_new_cart_item

def add_new_cart(data: Dict[str, str]):
    auth_token = request.headers.get('Authorization')
    if auth_token:
        resp = User.decode_auth_token(auth_token)
    user_id = Cart.query.filter_by(user_id=resp).first()
    if user_id:
        response_object = {
            'status': 'fail',
            'message': 'Cart already exists. Please Log in.',
        }
        return response_object, 409
    else:
        cart_id=str(uuid.uuid4())
        new_card = Cart(
            cart_id=cart_id,
            user_id=resp,
            quantity=int(data['quantity'])
        )
        save_changes(new_card)
        add_new_cart_item(cart_id, data)
        response_object = {
                'status': 'success',
                'message': 'successfully add new cart.',
                'card_item': {
                    "card_id": new_card.cart_id,
                    "user_id": new_card.user_id,
                    "quantity": new_card.quantity
                }
            }
        return response_object, 200

def save_changes(data: Cart):
    db.session.add(data)
    db.session.commit()