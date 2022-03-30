import uuid
from .. import db

class CartItem(db.Model):
    __tablename__= "cart_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    cart_item_id = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())
    product_id = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())

    quantity = db.Column(db.Integer, nullable=False)
    subtotal_ex_tax=db.Column(db.Float, nullable=True)
    tax_total=db.Column(db.Float, nullable=True)
    total=db.Column(db.Float, nullable=True)

    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))