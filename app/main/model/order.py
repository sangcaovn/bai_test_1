from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
from typing import Union


class Order(db.Model):
    __tablename__ = "order"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # order_cart = db.relationship('cart', backref='order',
    #                             lazy='dynamic')
    order_cart = db.Column(db.Integer)
    description = db.Column(db.Text)
    total = db.Column(db.Integer)

    def __repr__():
        return "Order"