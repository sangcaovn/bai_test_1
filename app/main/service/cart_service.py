
from urllib import response
from app.main import db
from app.main.model.cart import Cart
from app.main.model.cart_item import Cart_Item
from app.main.model.user import User
# from app.main.model.product import Product
from app.main.model.order import Order
from app.main.model.order_item import Order_Item

# from app.main.service.auth_helper import Auth
# from typing import Dict
# import uuid
# from flask import jsonify
from flask import request


def save_new_cart(data):

    auth_token = request.headers.get('Authorization')
    user_id = User.decode_auth_token(auth_token)
    quantity = data.get('item_quantity')
    product_id = data.get('product_id')
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        new_cart = Cart(
            user_id=user_id,
        )
        save_changes(new_cart)
        new_item = Cart_Item(
            quantity=quantity,
            cart_id=new_cart.cart_id,
            product_id=product_id
        )
        new_item.cal()
        new_cart.calcu()
        save_changes(new_item)
        new_i = {
            "product_id":new_item.product_id,
            "quantity":new_item.quantity,
            "subtotal_ex_tax":new_item.subtotal_ex_tax,
            "tax_total":new_item.tax_total,
            "total":new_item.total
        }
        lst =[new_i]
        response_object = {
            "user_id":new_cart.user_id,
            "cart_items":lst,
            "subtotal_ex_tax":new_cart.subtotal_ex_tax,
            "tax_total":new_cart.tax_total,
            "total":new_cart.total
        }
        return response_object,200
    else:
        lst = []
        cart_id=cart.cart_id
        cart_items = Cart_Item.query.filter_by(cart_id=cart_id).all()
        item_found = False
        for item in cart_items:
            if (item.product_id==product_id):
                item_found = True
                item.quantity += quantity
                item.cal()
                db.session.commit()
            new_i = {
                "product_id":item.product_id,
                "quantity":item.quantity,
                "subtotal_ex_tax":item.subtotal_ex_tax,
                "tax_total":item.tax_total,
                "total":item.total
                }
            lst.append(new_i)
        if not item_found:
            new_item = Cart_Item(
                quantity=quantity,
                cart_id=cart_id,
                product_id=product_id
            )
            new_item.cal()
            save_changes(new_item)
            new_i = {
                "product_id":new_item.product_id,
                "quantity":new_item.quantity,
                "subtotal_ex_tax":new_item.subtotal_ex_tax,
                "tax_total":new_item.tax_total,
                "total":new_item.total
                }
            lst.append(new_i)
        cart.calcu()
        response_object = {
            "user_id":cart.user_id,
            "cart_items":lst,
            "subtotal_ex_tax":cart.subtotal_ex_tax,
            "tax_total":cart.tax_total,
            "total":cart.total
        }
        return response_object, 200

def del_cart_item(data):
    cart_item = Cart_Item.query.filter_by(cart_item_id=data).first()
    if not cart_item:
        return "Not Found", 400
    else:
        db.session.delete(cart_item)
        db.session.commit()
        lst = []
        auth_token = request.headers.get('Authorization')
        user_id = User.decode_auth_token(auth_token)
        cart = Cart.query.filter_by(user_id=user_id).first()
        all_cart_item = Cart_Item.query.filter_by(cart_id=cart.cart_id).all()
        for item in all_cart_item:
            item.cal()
            new_i = {
                "product_id":item.product_id,
                "quantity":item.quantity,
                "subtotal_ex_tax":item.subtotal_ex_tax,
                "tax_total":item.tax_total,
                "total":item.total
                }
            lst.append(new_i)
        response_object = {
            "user_id":cart.user_id,
            "cart_items":lst,
            "subtotal_ex_tax":cart.subtotal_ex_tax,
            "tax_total":cart.tax_total,
            "total":cart.total
        }
        return response_object, 200

def change_qty(data,num):
    cart_item = Cart_Item.query.filter_by(cart_item_id=data).first()

    if not cart_item:
        return "Not Found", 400
    else:
        cart_item.change(num)
        db.session.commit()
        lst = []
        auth_token = request.headers.get('Authorization')
        user_id = User.decode_auth_token(auth_token)
        cart = Cart.query.filter_by(user_id=user_id).first()
        all_cart_item = Cart_Item.query.filter_by(cart_id=cart.cart_id).all()
        for item in all_cart_item:
            item.cal()
            new_i = {
                "product_id":item.product_id,
                "quantity":item.quantity,
                "subtotal_ex_tax":item.subtotal_ex_tax,
                "tax_total":item.tax_total,
                "total":item.total
                }
            lst.append(new_i)
        response_object = {
            "user_id":cart.user_id,
            "cart_items":lst,
            "subtotal_ex_tax":cart.subtotal_ex_tax,
            "tax_total":cart.tax_total,
            "total":cart.total
        }
        return response_object, 200

def cart_check_out():
    lst = []
    auth_token = request.headers.get('Authorization')
    user_id = User.decode_auth_token(auth_token)
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return "Dont have Cart",200
    cart.calcu()
    new_order = Order(
        user_id=cart.user_id,
        subtotal_ex_tax=cart.subtotal_ex_tax,
        tax_total=cart.tax_total,
        total=cart.total
    )
    save_changes(new_order)
    all_cart_item = Cart_Item.query.filter_by(cart_id=cart.cart_id).all()
    for item in all_cart_item:
        new_order_item = Order_Item(
            quantity=item.quantity,
            order_id=new_order.order_id,
            product_id=item.product_id,
            subtotal_ex_tax=item.subtotal_ex_tax,
            tax_total=item.tax_total,
            total=item.total
        )
        save_changes(new_order_item)
        new_or = {
            "quantity":new_order_item.quantity,
            "order_id":new_order_item.order_id,
            "product_id":new_order_item.product_id,
            "subtotal_ex_tax":new_order_item.subtotal_ex_tax,
            "tax_total":new_order_item.tax_total,
            "total":new_order_item.total
        }
        lst.append(new_or)
        db.session.delete(item)
        db.session.commit()
    response_object = {
        "user_id":new_order.user_id,
        "subtotal_ex_tax":new_order.subtotal_ex_tax,
        "tax_total":new_order.tax_total,
        "total":new_order.total,
        "order_items":lst
    }
    db.session.delete(cart)
    db.session.commit()
    return response_object,200

def save_changes(data: Cart):
    db.session.add(data)
    db.session.commit()

