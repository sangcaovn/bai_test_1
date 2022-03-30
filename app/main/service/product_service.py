
from app.main import db
from app.main.model.product import Product
from typing import Dict


def save_new_product(data: Dict[str, str]):
    product = Product.query.filter_by(id=data['product_id']).first()
    if not product:
        new_product = Product(
            product_id=data['product_id'],
            name=data['name'],
            price=data['price'],
            description=data['description']
        )
        save_changes(new_product)
        return new_product
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product already exists. Please Log in.',
        }
        return response_object, 409


def get_all_products():
    return Product.query.all()


def get_a_product(id):
    return Product.query.filter_by(product_id=id).first()


def save_changes(data: Product):
    db.session.add(data)
    db.session.commit()

