from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import relationship

from . import PaymentStatus
from .. import db, generate_uuid


class SharedFieldModel(object):
    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    quantity = db.Column(db.Integer, default=0)
    subtotal_ex_tax = db.Column(db.Float, default=0)
    tax_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    @declared_attr
    def user_id(self):
        return db.Column(db.String(100), db.ForeignKey('user.public_id'), unique=True)


class Cart(SharedFieldModel, db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    cart_items = relationship("CartItem", back_populates="cart")

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.id}'>"

    @classmethod
    def get_cart_by_user_id(cls, user_id: str):
        db_response = cls.query.filter_by(user_id=user_id).first()
        return db_response

    def to_order(self):
        order = Order(
            quantity=self.quantity,
            subtotal_ex_tax=self.subtotal_ex_tax,
            tax_total=self.tax_total,
            total=self.total
        )
        order.order_items = [cart_item.to_order_item(order.id) for cart_item in self.cart_items]
        return order


class Order(SharedFieldModel, db.Model):
    __tablename__ = 'order'

    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    payment_status = db.Column(db.Integer, default=PaymentStatus.INIT.value)
    order_items = db.relationship('OrderItem', back_populates='order', lazy='dynamic')

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.id}'>"
