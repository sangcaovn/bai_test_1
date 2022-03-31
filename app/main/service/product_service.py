
from app.main import db
from app.main.model.product import Product
from typing import Dict


def save_new_product(data: Dict[str, str]):
    product = Product.query.filter_by(name=data['name']).first()
    if not product:
        new_product = Product(
            name=data['name'],
            price=data['price']
        )
        save_changes(new_product)
        return "Done",201
    else:
        return "False", 409


def get_all_products():
    return Product.query.all()


def get_a_product(id):
    return Product.query.filter_by(id=id).first()


def save_changes(data: Product):
    db.session.add(data)
    db.session.commit()

