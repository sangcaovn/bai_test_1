from email.policy import default
from enum import unique
from .. import db
import uuid
class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())

    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    is_available = db.Column(db.Boolean, nullable=False, default=True)

    # Define relationship
    # cart_item = db.relationship("CartItem", uselist=False, backref="product")

    def __repr__(self):
        return "<Product '{}'>".format(self.name)