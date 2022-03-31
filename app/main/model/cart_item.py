
from enum import unique
from .. import db, flask_bcrypt
import datetime
from app.main.model.product import Product
from ..config import key
from typing import Union
import uuid


class Cart_Item(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_item_id = db.Column(db.String(100), unique=True,nullable=False, default=lambda:uuid.uuid4())
    quantity = db.Column(db.Integer)
    cart_id = db.Column(db.String(100),db.ForeignKey('cart.cart_id'), nullable=False)
    product_id = db.Column(db.String(100), nullable=False)
    subtotal_ex_tax = db.Column(db.Float,default=0)
    tax_total = db.Column(db.Float,default=0)
    total = db.Column(db.Float,default=0)

    def cal(self):
        self.subtotal_ex_tax = 0
        self.tax_total = 0
        self.total = 0
        prod = Product.query.filter_by(id=self.product_id).first()
        self.subtotal_ex_tax = self.quantity * prod.price
        self.tax_total = self.subtotal_ex_tax / 10
        self.total = self.subtotal_ex_tax + self.tax_total
    def change(self,num):
        self.quantity+=int(num)
        self.cal()