
from .. import db

class Order(db.Model):
    __tablename__="order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    order_uuid = db.Column(db.String(100), unique=True)
    user_uuid = db.Column(db.String(100), unique=True)
    payment_status=db.Column(db.String(100), nullable=True, default=None)
    
    subtotal_ex_tax=db.Column(db.Float, nullable=True, default= 0)
    tax_total=db.Column(db.Float, nullable=True, default= 0)
    total=db.Column(db.Float, nullable=True, default= 0)