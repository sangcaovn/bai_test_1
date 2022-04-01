import uuid
from .. import db

class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_at = db.Column(db.String(255))
    update_at = db.Column(db.DateTime, nullable=False)
    cart_uuid = db.Column(db.String(100), unique=True, default=lambda: uuid.uuid4())

    # Define relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cart_items = db.relationship("CartItem")
    
    def __repr__(self):
        return "<Cart '{}'>".format(self.cart_uuid)