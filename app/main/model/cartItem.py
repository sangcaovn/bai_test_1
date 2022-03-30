from sqlalchemy.ext.declarative.base import declared_attr

from .. import db


class SharedFieldModel(object):
    quantity = db.Column(db.Integer, default=1)
    subtotal_ex_tax = db.Column(db.Float, default=0)
    tax_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    @declared_attr
    def product_id(self):
        return db.Column(db.String(100), db.ForeignKey('product.product_id'))


class CartItem(SharedFieldModel, db.Model):
    __tablename__ = 'cartitem'

    cart_item_id = db.Column(db.String(100), primary_key=True)
    cart_id = db.Column(db.String(100), db.ForeignKey('cart.cart_id'))

    def __repr__(self):
        return "<Cart '{}'>".format(self.cart_id)


class OrderItem(SharedFieldModel, db.Model):
    __tablename__ = 'orderitem'

    order_item_id = db.Column(db.String(100), primary_key=True)
    order_id = db.Column(db.String(100), db.ForeignKey('order.order_id'))

    def __repr__(self):
        return "<Order '{}'>".format(self.order_id)
