import uuid
from .. import db

class Cart(db.Model):
    __tablename__="cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    cart_id = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())
    order_id = db.Column(db.String(100), unique=True, default=None)
    user_id = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())
    product_id = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    cart_items = db.relationship('CartItem', backref='cart', lazy='dynamic')
    subtotal_ex_tax=db.Column(db.Float, nullable=True)
    tax_total=db.Column(db.Float, nullable=True)
    total=db.Column(db.Float, nullable=True)

    payment_status=db.Column(db.String(100), nullable=True)