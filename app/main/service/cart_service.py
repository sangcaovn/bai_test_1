
from ast import Dict
from app.main import db
from flask import request

from app.main.model.cart import Cart
from app.main.model.user import User
from app.main.service.auth_helper import Auth
from typing import Dict

def get_login_user():
    data, status = Auth.get_logged_in_user(request)
    token = data.get('data')



def save_new_cart(data: Dict[str, str]):
    
    new_cart = Cart(
        product_id=data['productId'],
        quantity=data['quantity'],
    )
    return save_changes(new_cart)

def change_cart_quantity():
    pass

def checkout_cart():
    pass

def delete_cart_item():
    pass

def save_changes(data: Cart):
    db.session.add(data)
    db.session.commit()
