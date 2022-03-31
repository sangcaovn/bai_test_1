from .. import db, generate_uuid


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=True)

    cart_item = db.relationship("Product", back_populates="cart_item")

    def __repr__(self):
        return f'<Product: {self.name}>'
