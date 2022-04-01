from .. import db

class OrderDetail(db.Model):
    __tablename__ = "order_detail"

    id = db.Column(db.String, primary_key=True)
    product_id = db.Column(db.String(200), nullable=True)
    quantity = db.Column(db.Integer, nullable = False)
    subtotal_ex_tax = db.Column(db.Float, nullable=False)
    tax_total = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    # Define relationships
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    
    def __repr__(self):
        return "<Order Detail '{}'>".format(self.id)