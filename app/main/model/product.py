from .. import db

class Product(db.Model):

    __tablename__ = 'product'

    # product_id = db.Column(db.Integer, db.ForeignKey('cart.id'),primary_key=True)
    product_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60),unique=True)
    price = db.Column(db.Integer)
    description = db.Column(db.Text)

    def __repr__():
        return "Product"