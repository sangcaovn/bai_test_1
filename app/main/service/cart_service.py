from flask import request

from app.main import db
from app.main.model.cart import Cart
from app.main.model.cart_item import CartItem
from app.main.model.product import Product
from app.main.service.auth_helper import Auth


def get_cart_by_user_id(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()

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
            "payment_status": "string"}


def save_new_cart(data, customer):
    product = Product.query.filter_by(id=data.get("product_id")).first()
    if not product:
        return "Invalid input", 400

    cart = Cart.get_cart_by_user(user_id=customer.id)
    if cart:
        cart_items = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=data.get("product_id")
        ).all()
    else:
        cart = Cart(
            user_id=customer.id,
        )

    quantity = data.get("quantity")
    subtotal_ex_tax = product.price * quantity
    tax_total = subtotal_ex_tax * 0.1

    if len(cart_items) > 0:
        for itm in cart_items:
            itm.quantity += data.get("quantity")
    else:
        cart_item = CartItem(
            product_id=product.id,
            quantity=quantity,
            subtotal_ex_tax=subtotal_ex_tax,
            tax_total=tax_total,
            total=subtotal_ex_tax + tax_total,
            cart=cart
        )
        db.session.add(cart_item)

    cart.quantity += quantity
    cart.subtotal_ex_tax += subtotal_ex_tax
    cart.tax_total += tax_total
    cart.total += subtotal_ex_tax + tax_total

    # TODO: update calculate tax cart item
    db.session.add(cart)

    db.session.commit()

    # return data as required
    # TODO: this is placeholder return
    return get_cart_by_user_id(customer.id), 200


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
                return get_cart_by_user_id(user_uuid), 200

    return {"message": "Bad request!!!"}, 403


def checkout(user):
    cart_data = Cart.query.filter_by(user_id=user.id).first()
    if not cart_data:
        return "Bad request", 400

    order = cart_data.to_order()
    db.session.add(order)
    db.session.commit()

    # return data as required
    return get_cart_by_user_id(user.id), 200


def delete_cart_item(cart_item_uuid):
    user_uuid = Auth.get_cart_from_user_id(request)
    if user_uuid:
        cart_item = CartItem.query.filter_by(id=cart_item_uuid).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return get_cart_by_user_id(user_uuid), 200
        return "Resource not found", 404
    return {"message": "Bad request!!!"}, 403


def save_changes(data):
    db.session.add(data)
    db.session.commit()
