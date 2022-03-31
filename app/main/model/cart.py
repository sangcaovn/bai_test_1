from app.main.enum.type_enum import TypeEnum
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

    type=db.Column(db.String(50), default=lambda:TypeEnum.Cart.value)
    payment_status=db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return "<Cart '{}'>".format(self.cart_uuid)