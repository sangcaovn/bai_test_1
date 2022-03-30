from .. import db

class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_at = db.Column(db.String(255))
    update_at = db.Column(db.DateTime, nullable=False)

    # subtotal_ex_tax = db.Column(db.Float, nullable = False)
    # tax_total = db.Column(db.Float, nullable = False)
    # total = db.Column(db.Float, nullable = False)

    # Define relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cart_items = db.relationship("CartItem")
    
    def __repr__(self):
        return "<Product '{}'>".format(self.name)