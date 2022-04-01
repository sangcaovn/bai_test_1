import uuid
from .. import db

class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_at = db.Column(db.String(255))
    update_at = db.Column(db.DateTime, nullable=False)
    order_uuid = db.Column(db.String(100), unique=True)

    # Define relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_details = db.relationship("OrderDetail")

    payment_status=db.Column(db.String(100), nullable=True, default=lambda: 'INIT')
    
    def __repr__(self):
        return "<Order '{}'>".format(self.order_uuid)