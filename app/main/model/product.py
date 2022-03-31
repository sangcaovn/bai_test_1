from .. import db, generate_uuid


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String(100), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=True)

    cart_item = db.relationship("CartItem", back_populates="product")

    def to_response(self):
        return {
                "product_id": self.id,
                "name": self.name,
                "price": self.price
            }

    def __repr__(self):
        return f'<Product: {self.name}>'
