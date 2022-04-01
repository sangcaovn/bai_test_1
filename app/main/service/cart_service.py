
#import json
import uuid
from app.main import db
from flask import request#, jsonify
from app.main.enum.type_enum import TypeEnum
from app.main.model.cart_item import CartItem

from app.main.model.cart import Cart
from app.main.model.order import Order
from app.main.model.product import Product
from app.main.service.auth_helper import Auth

def save_new_cart(data):
    user_uuid=Auth.get_token_from_userid(request)
    if user_uuid:
        cart_data=Cart.query.filter_by(user_uuid=user_uuid).first()
        product=Product.get_product_by_uuid(data.get("productId"))
        if not product: 
            return {"message":"Product not found"}, 400

        if cart_data:
            cart_items=CartItem.query.filter_by(cart_id=cart_data.id,
            product_uuid=data.get("productId")).all()
            #print(f'{cart_items}')
            if cart_items:
                for itm in cart_items:
                    tmp=Product.get_product_by_uuid(itm.product_uuid)
                    quantity=itm.quantity + int(data.get("quantity"))
                    itm.quantity = quantity

                    sub_total=quantity*tmp.price
                    itm.subtotal_ex_tax=sub_total

                    tax_total=sub_total*0.1

                    itm.tax_total=tax_total
                    itm.total=sub_total+tax_total
            else:
                cart_item=CartItem()
                cart_item.cart_id=cart_data.id

                cart_item.product_uuid=data.get("productId")

                sub_total=int(data.get("quantity"))*product.price
                cart_item.subtotal_ex_tax=sub_total

                tax_total=sub_total*0.1
                cart_item.tax_total=tax_total

                cart_item.total=sub_total+tax_total
                cart_item.quantity=int(data.get("quantity"))
                db.session.add(cart_item)

            db.session.commit()
            cart_recalc(user_uuid)
            # return data
            return resp_print(user_uuid), 200
        else:
            cart_data=Cart()
            cart_data.cart_uuid = str(uuid.uuid4())
            cart_data.user_uuid = user_uuid

            cart_item = CartItem()
            cart_item.product_uuid=data.get("productId")

            sub_total=int(data.get("quantity"))*product.price
            cart_item.subtotal_ex_tax=sub_total

            cart_item.quantity=int(data.get("quantity"))
            tax_total=sub_total*0.1

            cart_item.tax_total=tax_total
            cart_item.total=sub_total+tax_total

            cart_data.cart_items.append(cart_item)
            save_changes(cart_data)
            # update cart price
            cart_recalc(user_uuid)
            return resp_print(user_uuid), 200

    return {"message":"Bad request!!!"}, 400

def change_cart_quantity(cart_item_id,data):
    user_uuid=Auth.get_token_from_userid(request)

    if not user_uuid:
        return {"message" : "PLease login"}, 403

    cart_item=CartItem.query.filter_by(cart_item_uuid=cart_item_id).first()
    if cart_item:
        product=Product.query.filter_by(product_uuid=cart_item.product_uuid).first()
        if not product:
            return {"message":"Product not found"}, 400

        # change values for cart-item
        cart_item.quantity = int(data.get("quantity"))
        #print(quantity)
        sub_total = cart_item.quantity*product.price
        cart_item.subtotal_ex_tax = sub_total

        tax_total = sub_total*0.1
        cart_item.tax_total = tax_total

        cart_item.total=sub_total+tax_total
        db.session.commit()

        # update cart price
        cart_recalc(user_uuid)
        return resp_print(user_uuid), 200

    return {"message":"Bad request!!!"}, 400

def checkout_cart():
    user_uuid=Auth.get_token_from_userid(request)
    if user_uuid:
        cart_data=Cart.query.filter_by(user_uuid=user_uuid).first()
        if cart_data:
            order_data= Order()
            order_data.payment_status="INIT"

            order_data.order_uuid = str(uuid.uuid4())
            order_data.user_uuid = cart_data.user_uuid
    
            order_data.subtotal_ex_tax = cart_data.subtotal_ex_tax
            order_data.tax_total = cart_data.tax_total
            order_data.total = cart_data.total 
            save_changes(order_data)
            cart_data.type = TypeEnum.Order.value
            #db.session.delete(cart_data)
            for itm in cart_data.cart_items:
                itm.type = TypeEnum.OrderDetail.value
                itm.cart_id = cart_data.id
    
            db.session.commit()
            # update cart price
            return resp_print(user_uuid), 200
    return {"message" : "PLease login"}, 403

def delete_cart_item(cart_item_uuid):
    user_uuid=Auth.get_token_from_userid(request)
    if user_uuid:

        cart_item=CartItem.query.filter_by(cart_item_uuid=cart_item_uuid).first()
        db.session.delete(cart_item)
        db.session.commit()
        # return data as required
        cart_recalc(user_uuid)
        return resp_print(user_uuid), 200

    return {"message" : "PLease login"}, 403

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def cart_recalc(user_uuid):

    cart= Cart.query.filter_by(user_uuid=user_uuid).first()
    cart_items=CartItem.query.filter_by(cart_id=cart.id).all()
    cart.subtotal_ex_tax = sum(row.subtotal_ex_tax for row in cart_items)
    cart.tax_total = sum(row.tax_total for row in cart_items)
    cart.total = sum(row.total for row in cart_items)
    db.session.commit()

def resp_print(user_uuid):
    order = Order.query.filter_by(user_uuid=user_uuid).first()
    cart= Cart.query.filter_by(user_uuid=user_uuid).first()
    cart_items=CartItem.query.filter_by(cart_id=cart.id).all()

    result = {
    'order_uuid' : order.order_uuid,
    'user_uuid' : order.user_uuid,
    'subtotal_ex_tax': 0,
    'tax_total': 0,
    'total': 0
    }
    list_order_items = []
    for data in cart_items:
        obj_item = {
            'order_item_id': data.cart_item_uuid,
            'product_id': data.product_uuid,
            'quantity': data.quantity,
            "subtotal_ex_tax": data.subtotal_ex_tax,
            'tax_total': data.tax_total,
            'total': data.total
        } 
    list_order_items.append(obj_item)
    result['order_items'] = list_order_items
    result['subtotal_ex_tax'] = sum(row.subtotal_ex_tax for row in cart_items)
    result['tax_total'] = sum(row.tax_total for row in cart_items)
    result['total'] = sum(row.total for row in cart_items)
    return result



    


