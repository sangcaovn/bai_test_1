
from app.main import db
from flask import request, jsonify
from app.main.model.cart_item import CartItem

from app.main.model.cart import Cart
from app.main.service.auth_helper import Auth

def get_cart_by_user_id(user_id):
    return Cart.query.filter_by(user_id==user_id).first()

def save_new_cart(data):
    user_id=Auth.get_cart_from_user_id(request)
    if user_id:
        cart_data=Cart.query.filter_by(user_id=user_id).first()
        if cart_data:
            cart_items=CartItem.query.filter_by(cart_id=cart_data.id,
            product_id=data.get("product_id")).all()
            if len(cart_items)>0:
                for itm in cart_items:
                    itm.quantity += data.get("quantity")
                    itm.save()
            else:
                product=Produc

                cart_item=CartItem()
                cart_items.cart_id=cart_data.id
                cart_items.cart_item_id=cart_data.cart_id
                cart_item.product_id=data.get("product_id")
                cart_item.subtotal_ex_tax=data.get("product_id")
                cart_item.tax_total=int(data.get("quantity"))*10
                cart_item.total=data.get("quantity")
                cart_item.quantity=int(data.get("quantity"))
                save_changes(cart_item)
                return jsonify(get_cart_by_user_id(user_id)), 200

    return {"message":"Bad request!!!"}, 403

def change_cart_quantity():
    pass

def checkout_cart():
    pass

def delete_cart_item():
    pass

def save_changes(data):
    db.session.add(data)
    db.session.commit()
