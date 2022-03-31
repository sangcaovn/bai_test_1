from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import relationship

from .. import db, generate_uuid


class SharedFieldModel(object):
    quantity = db.Column(db.Integer, default=1)
    subtotal_ex_tax = db.Column(db.Float, default=0)
    tax_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    @declared_attr
    def product(self):
        return db.relationship("Product")

    @declared_attr
    def product_id(self):
        return db.Column(db.ForeignKey('product.id'))


class CartItem(SharedFieldModel, db.Model):
    __tablename__ = 'cart_item'

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    cart_id = db.Column(db.ForeignKey('cart.id', ondelete="CASCADE"))

    cart = relationship("Cart", back_populates="cart_items")

    @classmethod
    def get_item_collection_by_cart_id(cls, cart_id: str):
        return cls.query.filter_by(cart_id=cart_id).all()

    def to_order_item(self, order_id):
        return OrderItem(
            quantity=self.quantity,
            subtotal_ex_tax=self.subtotal_ex_tax,
            tax_total=self.tax_total,
            total=self.total,
            order_id=order_id
        )


class OrderItem(SharedFieldModel, db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    order_id = db.Column(db.ForeignKey('order.id', ondelete="CASCADE"))

    order = relationship("Order", back_populates="order_items")

    def __repr__(self):
        return "<Order '{}'>".format(self.order_id)
