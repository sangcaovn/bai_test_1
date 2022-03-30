from enum import unique

from sqlalchemy.ext.declarative.base import declared_attr

from .. import db


class SharedFieldModel(object):
    quantity = db.Column(db.Integer, default=0)
    subtotal_ex_tax = db.Column(db.Float, default=0)
    tax_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    @declared_attr
    def user_id(self):
        return db.Column(db.String(100), db.ForeignKey('user.public_id'), unique=True)


class Cart(SharedFieldModel, db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.String(100), primary_key=True)
    cart_items = db.relationship('CartItem', backref='cart', lazy='dynamic')

    def __repr__(self):
        return f"<{self.__name__} '{self.cart_id}'>"


class Order(SharedFieldModel, db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.String(100), primary_key=True)
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def __repr__(self):
        return f"<{self.__name__} '{self.order_id}'>"
