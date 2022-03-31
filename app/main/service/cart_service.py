import json
import uuid
from typing import Dict

from app.main import db
from app.main.model.cart import Cart
from app.main.model.cartItem import CartItem
from .cartItem_service import create_a_cart_item, get_cart_item_list, formatCartItem
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
        quantity=int(data['quantity'])
        cartItem = CartItem.query.filter_by(cart_id=cart.cart_id,product_id=data['product_id'] ).first()
        product = Product.query.filter_by(product_id=data['product_id']).first()
        if not product:
            response_object = {
                'status': 'fail',
                'message': 'Product doesn\'t exists.',
                }
            return response_object, 404
        contentsTotal = product.price * quantity
        tax_total = contentsTotal * (10/100)
        if not cartItem :
            new_cartItem = CartItem(
                    cartItem_id=str(uuid.uuid4()),
                    cart_id=cart.cart_id,
                    product_id=data['product_id'],
                    quantity=int(data['quantity']),
                    subtotal_ex_tax=contentsTotal,
                    tax_total=tax_total,
                    total=contentsTotal+tax_total
                )
            db.session.add(new_cartItem)
            db.session.commit()
            cartItem = new_cartItem
        else:
            cartItem.quantity = cartItem.quantity + quantity
            cartItem.subtotal_ex_tax += contentsTotal
            cartItem.tax_total += tax_total
            cartItem.total += contentsTotal + tax_total
            db.session.add(cartItem)
            db.session.commit()
        data_cart_response = update_a_cart(cartItem.cart_id)
        if (data_cart_response[1] == 200):
            data_cart = data_cart_response[0]
            if 'data' not in data_cart:
                return data_cart_response
            else:
                cart = data_cart['data']
                cartitems = get_cart_item_list(cart['cart_id'])
                cartItems_result = formatCartItem(cartitems)
                response_object = {
                            'status': 'success',
                            'message': 'Successfully created.',
                            'data': {
                                "cart_id" : cart['cart_id'],
                                "quantity" : cart['quantity'],
                                "user_id" : cart['user_id'],
                                "cart_items" : cartItems_result,
                                "subtotal_ex_tax" : cart['subtotal_ex_tax'],
                                "tax_total" : cart['tax_total'],
                                "total" : cart['total']
                            } 
                        }
                return response_object, 201
        else:
            return data_cart_response
def update_a_cart(cart_id):
    cart = Cart.query.filter_by(cart_id=cart_id).first()
    if not cart:
        response_object = {
            'status': 'fail',
            'message': 'Cart doesn\'t exists.',
            }
        return response_object, 404
    cart_items = get_cart_item_list(cart_id)
    quantity = 0
    subtotal_ex_tax = 0
    tax_total = 0
    total = 0
    for cart_item in cart_items:
        quantity += cart_item.quantity
        subtotal_ex_tax += cart_item.subtotal_ex_tax
        tax_total += cart_item.tax_total
        total += cart_item.total
    cart.quantity = quantity
    cart.subtotal_ex_tax = subtotal_ex_tax
    cart.tax_total = tax_total
    cart.total = total

    save_changes (cart)
    response_object = {
                'status': 'success',
                'message': 'Successfully created.',
                'data': {
                    "cart_id" : cart.cart_id,
                    "quantity" : cart.quantity,
                    "user_id" : cart.user_id,
                    "subtotal_ex_tax" : cart.subtotal_ex_tax,
                    "tax_total" : cart.tax_total,
                    "total" : cart.total
                } 
            }
    return response_object, 200
def save_changes(data: Cart):
    db.session.add(data)
    db.session.commit()
