import uuid
from flask import request
from app.main import db
from app.main.model.cartitem import CartItem
from typing import Dict
from app.main.service.auth_helper import Auth
from app.main.model.user import User
from app.main.model.product import Product

def add_new_cart_item(cart_id, data: Dict[str, str]):
    cart_item = CartItem.query.filter_by(product_id = data['product_id'], cart_id=cart_id).first()
    
    if not cart_item:
        cart_item_id=str(uuid.uuid4())
        cart_id = cart_id
        product_id=data['product_id']
        quantity=int(data['quantity'])
        product = Product.query.filter_by(product_id = data['product_id']).first()
        print(product)
        subtotal_ex_tax=product.price*quantity
        tax_total = subtotal_ex_tax*10/100
        total = subtotal_ex_tax+tax_total
        new_card_item = CartItem(
            cart_item_id=cart_item_id,
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
            subtotal_ex_tax=subtotal_ex_tax,
            tax_total=tax_total,
            total=total
        )
        save_changes(new_card_item)
        response_object = {
                'status': 'success',
                'message': 'successfully add new cart item.',
            }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Cart item already exists. Please add a new product.',
        }
        return response_object, 409

def save_changes(data: CartItem):
    db.session.add(data)
    db.session.commit()