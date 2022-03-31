from .. import db
import uuid

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.String(60), primary_key=True, default=lambda:uuid.uuid4())
    name = db.Column(db.String(200), unique=True, nullable=False)
    price = db.Column(db.Integer)

    def __repr__(self):
        return "<Product '{}'>".format(self.name)