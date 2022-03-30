from __future__ import unicode_literals
from email.headerregistry import UniqueAddressHeader
from .. import db


class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Product '{}'>".format(self.name)
