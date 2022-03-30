import uuid
from .. import db

class Cart(db.Model):
    __tablename__="cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    cart_uuid = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())
    order_uuid = db.Column(db.String(100), unique=True, default=None)
    user_uuid = db.Column(db.String(100), unique=True)
    quantity = db.Column(db.Integer, nullable=True)
    cart_items = db.relationship('CartItem', backref='cart', lazy='dynamic')
    subtotal_ex_tax=db.Column(db.Float, nullable=True)
    tax_total=db.Column(db.Float, nullable=True)
    total=db.Column(db.Float, nullable=True)

    payment_status=db.Column(db.String(100), nullable=True)


    def __init__(self, data):
        self.cart_uuid = data.get("cart_uuid")
        self.order_uuid = data.get("order_uuid")
        self.user_uuid = data.get("user_uuid")
        self.quantity = data.get("quantity")
        self.subtotal_ex_tax = data.get("subtotal_ex_tax")
        self.tax_total = data.get("tax_total")
        self.total = data.get("total")