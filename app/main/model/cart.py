from dataclasses import dataclass

from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import relationship

from . import PaymentStatus
from .. import db, generate_uuid


class SharedFieldModel(object):

    @declared_attr
    def user_id(self):
        return db.Column(db.ForeignKey('user.id'), unique=True)


@dataclass
class Cart(SharedFieldModel, db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    cart_items = relationship("CartItem", back_populates="cart")

    def to_response(self):
        cart_items = []
        subtotal_ex_tax = 0
        tax_total = 0
        for item in self.cart_items:
            order_item = item.to_response()
            subtotal_ex_tax += order_item.get("subtotal_ex_tax")
            tax_total += order_item.get("tax_total")
            cart_items.append(order_item)
        return {
            "cart_id": self.id,
            "user_id": self.user_id,
            "cart_items": cart_items,
            "subtotal_ex_tax": subtotal_ex_tax,
            "tax_total": tax_total,
            "total": subtotal_ex_tax + tax_total
        }

    @classmethod
    def get_cart_by_user_id(cls, user):
        """Every customer can only have 1 cart at the time"""
        return cls.query.filter_by(user_id=user.id).first()

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.id}'>"

    @classmethod
    def get_cart_by_user(cls, user_id: str):
        db_response = cls.query.filter_by(user_id=user_id).first()
        return db_response

    def to_order(self):
        order = Order()
        order.order_items = [cart_item.to_order_item(order.id) for cart_item in self.cart_items]
        return order


class Order(SharedFieldModel, db.Model):
    __tablename__ = 'order'

    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    payment_status = db.Column(db.Integer, default=PaymentStatus.INIT.value)
    order_items = db.relationship('OrderItem', back_populates='order', lazy='dynamic')

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.id}'>"
