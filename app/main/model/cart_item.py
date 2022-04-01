from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import relationship

from .. import db, generate_uuid


class SharedFieldModel(object):
    quantity = db.Column(db.Integer, default=1)

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

    def to_response(self):
        subtotal_ex_tax = self.quantity * self.product.price
        tax_total = subtotal_ex_tax * 0.1
        return {
            "cart_item_id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "subtotal_ex_tax": subtotal_ex_tax,
            "tax_total": tax_total,
            "total": subtotal_ex_tax + tax_total
        }

    @classmethod
    def get_item_collection_by_cart_id(cls, cart_id: str):
        return cls.query.filter_by(cart_id=cart_id).all()

    def to_order_item(self, order_id):
        return OrderItem(
            product=self.product,
            quantity=self.quantity,
            order_id=order_id
        )


class OrderItem(SharedFieldModel, db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    order_id = db.Column(db.ForeignKey('order.id', ondelete="CASCADE"))

    order = relationship("Order", back_populates="order_items")

    def to_response(self):
        subtotal_ex_tax = self.quantity * self.product.price
        tax_total = subtotal_ex_tax * 0.1
        return {
            "order_item_id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "subtotal_ex_tax": subtotal_ex_tax,
            "tax_total": tax_total,
            "total": subtotal_ex_tax + tax_total
        }

    def __repr__(self):
        return "<Order '{}'>".format(self.order_id)
