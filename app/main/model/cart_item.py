import uuid

from app.main.enum.type_enum import TypeEnum
from .. import db

class CartItem(db.Model):
    __tablename__= "cart_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    cart_item_uuid = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())
    product_uuid = db.Column(db.String(100), unique=True)

    quantity = db.Column(db.Integer, nullable=False)
    subtotal_ex_tax=db.Column(db.Float, nullable=True)
    tax_total=db.Column(db.Float, nullable=True)
    total=db.Column(db.Float, nullable=True)

    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    type=db.Column(db.String(50), default=lambda:TypeEnum.CartItem.value)