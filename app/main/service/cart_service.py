
import json
import uuid
from app.main import db
from flask import request, jsonify
from app.main.enum.type_enum import TypeEnum
from app.main.model.cart_item import CartItem, CartItemSchema

from app.main.model.cart import Cart, CartSchema
from app.main.model.product import Product
from app.main.service.auth_helper import Auth

cart_schema=CartSchema()
cart_item_schema=CartItemSchema(many=True)

def response_data(user_uuid, payment_status=None):
    cart= Cart.query
    if payment_status:
        cart=cart.filter_by(order_user_uuid=user_uuid).filter_by(type=TypeEnum.Order.value).first()
    else:
        cart=cart.filter_by(user_uuid=user_uuid).first()
    obj= {
            "userId": user_uuid,
            "cart_items": None,
            "subtotal_ex_tax": 0,
            "tax_total": 0,
            "total": 0
        }

    obj["subtotal_ex_tax"]=sum(row.subtotal_ex_tax for row in cart.cart_items)
    obj["tax_total"]=sum(row.tax_total for row in cart.cart_items)
    obj["total"]=sum(row.total for row in cart.cart_items)
    obj["cart_items"]=json.loads(cart_item_schema.dumps(cart.cart_items))
    if payment_status:
        obj["order_id"]=cart.cart_uuid
        obj["payment_status"]=payment_status
    else:
        obj["cart_id"]=cart.cart_uuid
    return obj

def save_new_cart(data):
    user_uuid=Auth.get_cart_from_user_id(request)
    if user_uuid:
        cart_data=Cart.query \
            .filter_by(type=TypeEnum.Cart.value) \
            .filter_by(user_uuid=user_uuid).first()
        product=Product.get_product_by_uuid(data.get("productId"))
        if not product: 
            return {"message":"could not found product with input id!!!"}, 403

        if cart_data:
            cart_items=CartItem.query.filter_by(cart_id=cart_data.id,
            product_uuid=data.get("productId")).all()
            if cart_items:
                for itm in cart_items:
                    tmp=Product.get_product_by_uuid(itm.product_uuid)
                    quantity=itm.quantity + int(data.get("quantity"))
                    itm.quantity = quantity

                    sub_total=quantity*tmp.price
                    itm.subtotal_ex_tax=sub_total

                    tax_total=(sub_total*10)/100

                    itm.tax_total=tax_total
                    itm.total=sub_total+tax_total
            else:
                cart_item=CartItem()
                cart_items.cart_id=cart_data.id

                cart_item.product_uuid = data.get("productId")
                cart_item.order_product_uuid =data.get("productId")
                cart_item.subtotal_ex_tax=int(data.get("quantity"))

                sub_total=int(data.get("quantity"))*product.price
                cart_item.subtotal_ex_tax=sub_total

                tax_total=(sub_total*10)/100
                cart_item.tax_total=tax_total

                cart_item.total=sub_total+tax_total
                cart_item.quantity=int(data.get("quantity"))
                db.session.add(cart_item)

            db.session.commit()

            # return data as required
            return response_data(user_uuid), 200
        else:
            cart_data=Cart()
            cart_data.cart_uuid=uuid.uuid4()
            cart_data.user_uuid=user_uuid
            cart_data.order_user_uuid=user_uuid

            cart_item=CartItem()
            cart_item.product_uuid=data.get("productId")
            cart_item.order_product_uuid=data.get("productId")

            sub_total=int(data.get("quantity"))*product.price
            cart_item.subtotal_ex_tax=sub_total

            cart_item.quantity=int(data.get("quantity"))
            tax_total=(sub_total*10)/100
            cart_item.tax_total=tax_total
            cart_item.total=sub_total+tax_total

            cart_data.cart_items.append(cart_item)
            save_changes(cart_data)

            # return data as required
            return response_data(user_uuid), 200

    return {"message":"Bad request!!!"}, 403

def change_cart_quantity(cart_item_id,data):
    user_uuid=Auth.get_cart_from_user_id(request)
    if not user_uuid:
        return {"message":"Bad request!!!"}, 403

    cart_item=CartItem.query \
        .filter_by(type=TypeEnum.CartItem.value) \
        .filter_by(cart_item_uuid=cart_item_id).first()
    if cart_item:
        product=Product.query.filter_by(product_uuid=cart_item.product_uuid).first()
        if not product:
            return {"message":"Bad request!!!"}, 403

        # calculate values for cart-item
        quantity=cart_item.quantity + int(data.get("quantity"))
        sub_total=quantity*product.price
        cart_item.subtotal_ex_tax = sub_total

        tax_total=(sub_total*10)/100
        cart_item.tax_total =tax_total

        cart_item.total=sub_total+tax_total
        cart_item.quatity=int(data.get("quantity"))


        
        db.session.commit()

        # return data as required
        return response_data(user_uuid), 200

    return {"message":"Bad request!!!"}, 403

def checkout_cart():
    user_uuid=Auth.get_cart_from_user_id(request)
    if user_uuid:
        cart_data=Cart.query \
            .filter_by(type=TypeEnum.Cart.value) \
            .filter_by(user_uuid=user_uuid) \
            .first()
        if cart_data:
            cart_data.type=TypeEnum.Order.value
            cart_data.payment_status="INIT"

            cart_data.user_uuid=uuid.uuid4()
            
            for itm in cart_data.cart_items:
                itm.type=TypeEnum.OrderDetail.value
                itm.product_uuid=uuid.uuid4()
                
            db.session.commit()

            # return data as required
            return response_data(user_uuid,"INIT"), 200
    return {"message":"Bad request!!!"}, 403

def delete_cart_item(cart_item_uuid):
    user_uuid=Auth.get_cart_from_user_id(request)
    if user_uuid:
        cart_item=CartItem.query \
            .filter_by(type=TypeEnum.CartItem.value) \
            .filter_by(cart_item_uuid=cart_item_uuid).first()
        db.session.delete(cart_item)
        
        db.session.commit()

        # return data as required
        return response_data(user_uuid), 200

    return {"message":"Bad request!!!"}, 403

def save_changes(data):
    db.session.add(data)
    db.session.commit()
