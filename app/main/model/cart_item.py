from app.main.enum.type_enum import TypeEnum
from .. import db
import uuid


class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.String, primary_key=True, autoincrement=True)


    product_id = db.Column(db.String(200), nullable=True)

    quantity = db.Column(db.Integer, nullable = False)
    subtotal_ex_tax = db.Column(db.Float, nullable=False)
    tax_total = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    # Define relationships
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    type=db.Column(db.String(50), default=lambda:TypeEnum.CartItem.value)


    #product_name = db.Column(db.String, db.ForeignKey('product.name'))
    #product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    def __repr__(self):
        return "<Cart Item '{}'>".format(self.id)