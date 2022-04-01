from flask import request

from app.main import db
from app.main.model.cart import Cart, Order
from app.main.model.cart_item import CartItem
from app.main.model.product import Product
from app.main.service.auth_helper import Auth


def get_cart_by_user_id(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    return cart.to_response()


def save_new_cart(data, customer):
    product = Product.query.filter_by(id=data.get("product_id")).first()
    if not product:
        return "Invalid input", 400

    cart = Cart.get_cart_by_user(user_id=customer.id)
    cart_items = []
    if cart:
        cart_items = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=data.get("product_id")
        ).all()
    else:
        cart = Cart(user_id=customer.id)

    quantity = data.get("quantity")

    if len(cart_items) > 0:
        for itm in cart_items:
            itm.quantity += data.get("quantity")
    else:
        cart_item = CartItem(
            product_id=product.id,
            quantity=quantity,
            cart=cart
        )
        db.session.add(cart_item)
    db.session.add(cart)
    db.session.commit()
    return get_cart_by_user_id(customer.id), 200


def change_cart_quantity(cart_item_id, data, user):
    cart_data = Cart.query.filter_by(user_id=user.id).first()

    if not cart_data:
        return {"message": "Cart not found"}, 404

    cart_item = CartItem.query.filter_by(id=cart_item_id).first()
    if not cart_item:
        return {"message": "Cart item not found"}, 404

    cart_item.quantity = data.get("quantity")
    db.session.commit()
    return get_cart_by_user_id(user.id), 200


def checkout(user):
    cart_data = Cart.query.filter_by(user_id=user.id).first()
    if not cart_data:
        return "Cart not found", 400

    if len(cart_data.cart_items) < 1:
        return "Cart is empty", 400
    order = cart_data.to_order()
    db.session.add(order)
    db.session.delete(cart_data)
    db.session.commit()

    return order.to_response(), 200


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
