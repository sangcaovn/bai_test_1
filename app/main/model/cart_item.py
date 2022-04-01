import uuid
from marshmallow import Schema, fields
from app.main.enum.type_enum import TypeEnum
from .. import db

class CartItem(db.Model):
    __tablename__= "cart_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    cart_item_uuid = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())
    product_uuid = db.Column(db.String(100), unique=True)
    order_product_uuid = db.Column(db.String(100))

    quantity = db.Column(db.Integer, nullable=False)
    subtotal_ex_tax=db.Column(db.Float, nullable=True)
    tax_total=db.Column(db.Float, nullable=True)
    total=db.Column(db.Float, nullable=True)

    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    type=db.Column(db.String(50), default=lambda:TypeEnum.CartItem.value)

class CartItemSchema(Schema):
    cart_item_uuid = fields.String(data_key="cart_item_id")
    product_uuid = fields.String(data_key="product_id")
    quantity = fields.Integer()
    subtotal_ex_tax = fields.Integer()
    tax_total = fields.Integer()
    total = fields.Integer()