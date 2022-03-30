from .. import db
import uuid

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_uuid = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=True)

    cart = db.relationship("Product", back_populates="cart_item")

    def __init__(self, data):
        self.name = data.get("name")
        self.price = data.get("price")
        self.product_uuid = data.get("product_uuid")

    def __repr__(self):
        return '<Product: {}'.format(self.name)
