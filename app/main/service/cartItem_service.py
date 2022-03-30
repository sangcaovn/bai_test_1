import json
import uuid
from typing import Dict

from app.main import db
from app.main.model.cartItem import CartItem

def create_a_cart_item(cart, data: Dict[str, str]):
    cartItem = CartItem.query.filter_by(product_id = data['product_id'], cart_id=cart.cart_id).first()
    if not cartItem:
        new_cartItem = CartItem(
                    cartItem_id=str(uuid.uuid4()),
                    cart_id=cart.cart_id,
                    product_id=data['product_id'],
                    quantity=int(data['quantity']),
                    subtotal_ex_tax=cart.subtotal_ex_tax,
                    tax_total=cart.tax_total,
                    total=cart.total
                )
        save_changes(new_cartItem)
        response_object = {
            'status': 'success',
            'message': 'Successfully created.',
            'data': {
                "cartItem_id" : new_cartItem.cartItem_id,
                "cart_id" : new_cartItem.cart_id,
                "quantity" : new_cartItem.quantity,
                "product_id" : new_cartItem.product_id,
                "subtotal_ex_tax" : new_cartItem.subtotal_ex_tax,
                "tax_total" : new_cartItem.tax_total,
                "total" : new_cartItem.total
            } 
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Cart item already exists.',
        }
        return response_object, 409
def save_changes(data: CartItem):
    db.session.add(data)
    db.session.commit()