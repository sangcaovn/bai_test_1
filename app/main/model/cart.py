
from enum import unique
from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from app.main.model.cart_item import Cart_Item
from ..config import key
from typing import Union
import uuid


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100),unique=True,nullable=False)
    cart_id = db.Column(db.String(100), unique=True,nullable=False, default=lambda:uuid.uuid4())
    subtotal_ex_tax = db.Column(db.Float,default=0)
    tax_total = db.Column(db.Float,default=0)
    total = db.Column(db.Float,default=0)
    
    cart_items = db.relationship('Cart_Item', backref = 'cart', lazy='dynamic')

    def calcu(self):
        self.subtotal_ex_tax = 0
        self.tax_total = 0
        self.total = 0
        all_item = Cart_Item.query.filter_by(cart_id=self.cart_id).all()
        for item in all_item:
            self.subtotal_ex_tax+=int(item.subtotal_ex_tax)
            self.tax_total+=int(item.tax_total)
            self.total+=int(item.total)