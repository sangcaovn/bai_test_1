
from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
from typing import Union


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_quantity = db.Column(db.Integer)
    # cart_items = db.relationship('product', backref='cart',
    #                             lazy='dynamic')
    cart_items = db.Column(db.Text)
    def __repr__():
        return "Cart"