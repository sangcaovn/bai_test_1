from .. import db, flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
from typing import Union
import uuid

class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100),nullable=False)
    order_id = db.Column(db.String(100), unique=True,nullable=False, default=lambda:uuid.uuid4())
    subtotal_ex_tax = db.Column(db.Float)
    tax_total = db.Column(db.Float)
    total = db.Column(db.Float)
    payment_status = db.Column(db.Integer, default=0)
    
    order_items = db.relationship('Order_Item', backref = 'order', lazy='dynamic')
    def __repr__(self):
        return "<Order '{}'>".format(self.order_id)