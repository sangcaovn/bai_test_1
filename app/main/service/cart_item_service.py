import json
from app.main import db
from flask import jsonify
from app.main.model.cart_item import CartItem
import datetime
from typing import Dict
import uuid

from app.main.model.cart_item import CartItem
from app.main.model.product import Product

def get_cart_item(cart_item_id: str):
    return CartItem.query.filter_by(id=cart_item_id).first()

def save_new_item(cart_id: int, data: Dict[str, str]):
    product_id = data['cart_items'][0]['product_id']
    product = Product.query.filter_by(public_id=product_id).first()
    if not product:
        return "Product not found", 404

    existed_cart_item = filter_multiple_fields(cart_id, product_id)
    if not existed_cart_item:
        price = product.price
        subtotal_ex_tax = int(data['cart_items'][0]['quantity']) * price
        tax_total = subtotal_ex_tax * 0.1
        total = subtotal_ex_tax + tax_total

        new_cart_item = CartItem(
                id=str(uuid.uuid4()),
                product_id = product_id,
                quantity=data['cart_items'][0]['quantity'],
                subtotal_ex_tax= subtotal_ex_tax,
                tax_total=tax_total,
                total = total,
                cart_id = cart_id
            )
        save_changes(new_cart_item)
    else:    
        existed_quantity = existed_cart_item.quantity
        new_quantity = existed_quantity + 1
        update_change(cart_id, product_id, new_quantity)

    return 'success', 201
   

def filter_multiple_fields(cart_id, product_id):
    cart_items = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
    return cart_items

def update_quantity(cart_item_id, data):
    new_quantity = data['quantity']
    existed_cart_item = CartItem.query.filter_by(id = cart_item_id).first()
    if not existed_cart_item:
        return "Cart item not found", 404
    
    product_id = existed_cart_item.product_id
    product = Product.query.filter_by(public_id=product_id).first()
    price = product.price

    # Update the taxes
    subtotal_ex_tax = new_quantity * price
    tax_total = subtotal_ex_tax * 0.1
    total = subtotal_ex_tax + tax_total

    update_change_quantity_taxes(cart_item_id, new_quantity, subtotal_ex_tax, tax_total, total)

    return "success", 200

def save_changes(cart_item: CartItem):
    db.session.add(cart_item)
    db.session.commit()

def update_change(cart_id, product_id, new_quantity):
    num_rows_updated = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).update(dict(quantity=new_quantity))
    db.session.commit()

def update_change_quantity_taxes(cart_item_id, new_quantity, subtotal_ex_tax, tax_total, total):
    num_rows_updated = CartItem.query.filter_by(id=cart_item_id).update(
        dict(
            quantity=new_quantity,
            subtotal_ex_tax = subtotal_ex_tax,
            tax_total = tax_total,
            total = total
            )
        )
    db.session.commit()

def delete_cart_item(cart_item_id):
    CartItem.query.filter_by(id=cart_item_id).delete()
    db.session.commit()

    return 'deleted successfully!', 200