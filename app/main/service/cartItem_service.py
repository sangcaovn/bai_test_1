import json
import uuid
from typing import Dict

from app.main import db
from app.main.model.cartItem import CartItem
from app.main.model.product import Product
from app.main.model.cart import Cart


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
def update_a_cart_item(cartItem_id, data: Dict[str, str]):
    quantity=int(data['quantity'])
    #Check if cart item quantity = 0 delete cart item, check ìf no cart item in cart, delete cart
    cartItem = CartItem.query.filter_by(cartItem_id = cartItem_id).first()
    if not cartItem :
        response_object = {
            'status': 'fail',
            'message': 'Cart item doesn\'t exists.',
            }
        return response_object, 404
    product = Product.query.filter_by(product_id=cartItem.product_id).first()
    if not product:
        response_object = {
            'status': 'fail',
            'message': 'Product doesn\'t exists.',
            }
        return response_object, 404
    if (quantity == 0):
        pass
    cartItem.quantity = quantity
    contentsTotal = product.price * quantity
    tax_total = contentsTotal * (10/100)
    cartItem.subtotal_ex_tax = contentsTotal
    cartItem.tax_total = tax_total
    cartItem.total = contentsTotal + tax_total
    #Change cart item, change cart (quantity, subtax, tax, total)
    save_changes (cartItem)
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
            return response_object, 200
    else:
        return data_cart_response
def get_cart_item_list(cart_id):
    return CartItem.query.filter_by(cart_id=cart_id).all()
def delete_cart_item(cartItem_id):
    cartItem = CartItem.query.filter_by(cartItem_id = cartItem_id).first()
    if not cartItem :
        response_object = {
            'status': 'fail',
            'message': 'Cart item doesn\'t exists.',
            }
        return response_object, 404
    db.session.delete(cartItem)
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
            return response_object, 200
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

    if cart.quantity > 0:
        db.session.add(cart)
        db.session.commit()
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
    else:
        db.session.delete(cart)
        db.session.commit()
        response_object = {
                    'status': 'success',
                    'message': 'Successfully deleted.',
                }
        return response_object, 200
def save_changes(data: CartItem):
    db.session.add(data)
    db.session.commit()
def formatCartItem(cartItems):
    cartItems_result = []
    for cartItem in cartItems:
        cartItems_result.append({
            "cartItem_id" : cartItem.cartItem_id,
            "cart_id" : cartItem.cart_id,
            "quantity" : cartItem.quantity,
            "product_id" : cartItem.product_id,
            "subtotal_ex_tax" : cartItem.subtotal_ex_tax,
            "tax_total" : cartItem.tax_total,
            "total" : cartItem.total
        })
    return cartItems_result