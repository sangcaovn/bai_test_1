from enum import unique
from .. import db, flask_bcrypt
from ..config import key
from typing import Union
import uuid


class Order_Item(db.Model):
    __tablename__ = "order_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_item_id = db.Column(db.String(100), unique=True,nullable=False, default=lambda:uuid.uuid4())
    quantity = db.Column(db.Integer)
    order_id = db.Column(db.String(100),db.ForeignKey('order.order_id'), nullable=False)
    product_id = db.Column(db.String(100), nullable=False)
    subtotal_ex_tax = db.Column(db.Float)
    tax_total = db.Column(db.Float)
    total = db.Column(db.Float)
