import json
import uuid
from typing import Dict

from app.main import db
from app.main.model.cart import Cart
from app.main.model.cartItem import CartItem
from .cartItem_service import create_a_cart_item
from app.main.model.product import Product

def create_a_cart(user_id, data: Dict[str, str]):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        product = Product.query.filter_by(product_id=data['product_id']).first()
        if product:
            contentsTotal = product.price * int(data['quantity'])
            tax_total = contentsTotal*(10/100)
            new_cart = Cart(
                cart_id=str(uuid.uuid4()),
                user_id=user_id,
                quantity=int(data['quantity']),
                subtotal_ex_tax=contentsTotal,
                tax_total=tax_total,
                total=contentsTotal+tax_total
            )
            save_changes(new_cart)
            data_cartitem_response = create_a_cart_item(new_cart, data)
            data_cartitem = data_cartitem_response[0]
            cartitem = data_cartitem['data']

            response_object = {
                'status': 'success',
                'message': 'Successfully created.',
                'data': {
                    "cart_id" : new_cart.cart_id,
                    "quantity" : new_cart.quantity,
                    "user_id" : new_cart.user_id,
                    "cart_items" : cartitem,
                    "subtotal_ex_tax" : new_cart.subtotal_ex_tax,
                    "tax_total" : new_cart.tax_total,
                    "total" : new_cart.total
                } 
            }
            return response_object, 201
        else:
            response_object = {
            'status': 'fail',
            'message': 'Product doesn\'t exists.',
            }
            return response_object, 404
    else:
        response_object = {
            'status': 'fail',
            'message': 'Cart already exists.',
        }
        return response_object, 409
def save_changes(data: Cart):
    db.session.add(data)
    db.session.commit()