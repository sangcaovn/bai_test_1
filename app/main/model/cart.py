import uuid

from app.main.enum.type_enum import TypeEnum
from .. import db

class Cart(db.Model):
    __tablename__="cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    cart_uuid = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())
    user_uuid = db.Column(db.String(100), unique=True)
    cart_items = db.relationship('CartItem', backref='cart', lazy='dynamic')

    type=db.Column(db.String(50), default=lambda:TypeEnum.Cart.value)
    #payment_status=db.Column(db.String(100), nullable=True, default=None)

    subtotal_ex_tax=db.Column(db.Float, nullable=True, default= 0)
    tax_total=db.Column(db.Float, nullable=True, default= 0)
    total=db.Column(db.Float, nullable=True, default= 0)