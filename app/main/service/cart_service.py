from flask import request, jsonify

from app.main import db
from app.main.model.cart import Cart
from app.main.model.cart_item import CartItem
from app.main.model.product import Product
from app.main.service.auth_helper import Auth


def get_cart_by_user_id(user_id):
    cart = Cart.query.filter_by(user_id == user_id).first()

    return {"order_id": "string",
            "userId": "string",
            "cart_items": [
                {
                    "order_item_id": "string",
                    "product_id": "518e8af7-6617-42a3-a227-b9be1b70fec8",
                    "quantity": 3,
                    "subtotal_ex_tax": 0,
                    "tax_total": 0,
                    "total": 0
                }
            ],
            "subtotal_ex_tax": 0,
            "tax_total": 0,
            "total": 0,
            "payment_status": "string"}, 200


def save_new_cart(data):
    user_uuid = Auth.get_cart_from_user_id(request)
    if user_uuid:
        cart_data = Cart.query.filter_by(user_uuid=user_uuid).first()
        if cart_data:
            cart_items = CartItem.query.filter_by(cart_id=cart_data.id,
                                                  product_uuid=data.get("product_id")).all()
            if len(cart_items) > 0:
                for itm in cart_items:
                    itm.quantity += data.get("quantity")
                    itm.save()
            else:
                product = Product.query.filter_by(product_uuid=data.get("product_id")).first()

                cart_item = CartItem()
                cart_items.cart_id = cart_data.id
                cart_items.cart_item_uuid = cart_data.cart_id
                cart_item.product_uuid = data.get("product_id")
                cart_item.subtotal_ex_tax = int(data.get("quantity"))

                if product:
                    cart_item.tax_total = int(data.get("quantity")) * product.price
                else:
                    cart_item.tax_total = int(data.get("quantity"))
                cart_item.total = data.get("quantity")
                cart_item.quantity = int(data.get("quantity"))
                db.session.add(cart_item)

                db.session.commit()

                # return data as required
                return jsonify(get_cart_by_user_id(user_uuid)), 200

    return {"message": "Bad request!!!"}, 403


def change_cart_quantity(cart_item_id, data):
    user_uuid = Auth.get_cart_from_user_id(request)
    if user_uuid:
        cart_data = Cart.query.filter_by(user_uuid=user_uuid).first()
        if cart_data:
            cart_item = CartItem.query.filter_by(cart_item_uuid=cart_item_id).first()
            if cart_item:

                product = Product.query.filter_by(product_uuid=data.get("product_id")).first()
                # calculate values for cart-item
                cart_item.quantity += data.get("quantity")

                cart_item.subtotal_ex_tax = int(data.get("quantity"))

                if product:
                    cart_item.tax_total = int(data.get("quantity")) * product.price
                else:
                    cart_item.tax_total = int(data.get("quantity"))
                cart_item.total = data.get("quantity")
                cart_item.quantity = int(data.get("quantity"))

                cart_item.save()

                db.session.commit()

                # return data as required
                return jsonify(get_cart_by_user_id(user_uuid)), 200

    return {"message": "Bad request!!!"}, 403


def checkout_cart():
    user_uuid = Auth.get_cart_from_user_id(request)
    if user_uuid:
        cart_data = Cart.query.filter_by(user_uuid=user_uuid).first()
        if cart_data:
            cart_data.type = TypeEnum.Order.value
            cart_data.payment_status = "INIT"
            cart_data.save()
            for itm in cart_data.cart_items:
                itm.type = TypeEnum.OrderDetail.value
                itm.save()
            db.session.commit()

            # return data as required
            return jsonify(get_cart_by_user_id(user_uuid)), 200
    return {"message": "Bad request!!!"}, 403


def delete_cart_item(cart_item_uuid):
    user_uuid = Auth.get_cart_from_user_id(request)
    if user_uuid:
        cart_data = Cart.query.filter_by(user_uuid=user_uuid).first()
        if cart_data:
            cart_item = CartItem.query.filter_by(cart_item_uuid=cart_item_uuid).first()
            db.session.delete(cart_item)

            db.session.commit()

            # return data as required
            return jsonify(get_cart_by_user_id(user_uuid)), 200

    return {"message": "Bad request!!!"}, 403


def save_changes(data):
    db.session.add(data)
    db.session.commit()
