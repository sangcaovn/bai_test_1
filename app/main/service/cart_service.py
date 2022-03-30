
from app.main import db
from flask import request, jsonify
from app.main.model.cart_item import CartItem

from app.main.model.cart import Cart
from app.main.model.product import Product
from app.main.service.auth_helper import Auth

def get_cart_by_user_id(user_id):
    return Cart.query.filter_by(user_id==user_id).first()

def save_new_cart(data):
    user_id=Auth.get_cart_from_user_id(request)
    if user_id:
        cart_data=Cart.query.filter_by(user_id=user_id).first()
        if cart_data:
            cart_items=CartItem.query.filter_by(cart_id=cart_data.id,
            product_uuid=data.get("product_id")).all()
            if len(cart_items)>0:
                for itm in cart_items:
                    itm.quantity += data.get("quantity")
                    itm.save()
            else:
                product=Product.query.filter_by(product_uuid=data.get("product_id")).first()

                cart_item=CartItem()
                cart_items.cart_id=cart_data.id
                cart_items.cart_item_uuid=cart_data.cart_id
                cart_item.product_uuid=data.get("product_id")
                cart_item.subtotal_ex_tax=int(data.get("quantity"))

                if product:
                    cart_item.tax_total=int(data.get("quantity"))*product.price
                else:
                    cart_item.tax_total=int(data.get("quantity"))
                cart_item.total=data.get("quantity")
                cart_item.quantity=int(data.get("quantity"))
                save_changes(cart_item)

                # return data as required
                return jsonify(get_cart_by_user_id(user_id)), 200

    return {"message":"Bad request!!!"}, 403

def change_cart_quantity(cart_item_id,json_data):
    pass

def checkout_cart():
    pass

def delete_cart_item(cart_item_id):
    pass

def save_changes(data):
    db.session.add(data)
    db.session.commit()
