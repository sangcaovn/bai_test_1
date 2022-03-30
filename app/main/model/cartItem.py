from .. import db

class CartItem(db.Model):
    __tablename__ = 'cartitem'

    cartItem_id = db.Column(db.String(100), primary_key=True)
    product_id = db.Column(db.String(100), db.ForeignKey('product.product_id'))
    cart_id = db.Column(db.String(100), db.ForeignKey('cart.cart_id'))
    quantity = db.Column (db.Integer, default=1)
    subtotal_ex_tax = db.Column(db.Float,  default=0)
    tax_total = db.Column(db.Float,  default=0)
    total = db.Column(db.Float,  default=0)
    def __repr__(self):
        return "<Cart '{}'>".format(self.cart_id)

