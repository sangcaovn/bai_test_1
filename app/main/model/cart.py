from marshmallow import Schema, fields
import uuid

from app.main.enum.type_enum import TypeEnum
from app.main.model.cart_item import CartItemSchema
from .. import db

class Cart(db.Model):
    __tablename__="cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    cart_uuid = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())
    user_uuid = db.Column(db.String(100), unique=True)
    cart_items = db.relationship('CartItem', backref='cart', lazy='dynamic')

    type=db.Column(db.String(50), default=lambda:TypeEnum.Cart.value)
    payment_status=db.Column(db.String(100), nullable=True, default=None)


    # def __init__(self, data):
    #     self.cart_uuid = data.get("cart_uuid")
    #     self.order_uuid = data.get("order_uuid")
    #     self.user_uuid = data.get("user_uuid")

class CartSchema(Schema):
    id = fields.Integer()
    cart_uuid = fields.String()
    user_uuid = fields.String()
    cart_items=fields.Nested(CartItemSchema)