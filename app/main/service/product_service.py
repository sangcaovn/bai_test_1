import uuid

from app.main import db
from app.main.model.product import Product
from typing import Dict


def create_a_product(data: Dict[str, str]):
    product = Product.query.filter_by(name=data['name']).first()
    if not product:
        new_product = Product(
            id=str(uuid.uuid4()),
            name=data['name'],
            price=int(data['price'])
        )
        save_changes(new_product)
        response_object = {
            'status': 'success',
            'message': 'Successfully created.',
            'data': {
                "product_id": new_product.id,
                "name": new_product.name,
                "price": new_product.price
            }
        }
        return response_object, 201
    else:
        return {"message": "Invalid input"}, 400


def get_product_list():
    return Product.query.all()


def get_a_product(name):
    return Product.query.filter_by(name=name).first()


def update_a_product(name, data: Dict[str, str]):
    product = Product.query.filter_by(name=name).first()
    if not product:
        response_object = {
            'status': 'fail',
            'message': 'Product not exists.',
        }
        return response_object, 404
    else:
        if ('name' in data):
            product = Product.query.filter_by(name=data['name']).first()
            if product:
                response_object = {
                    'status': 'fail',
                    'message': 'Product name already exists.',
                }
                return response_object, 409
            product.name = data['name']
        if ('description' in data):
            product.description = data['description']
        if ('price' in data):
            product.price = int(data['price'])
        save_changes(product)
        response_object = {
            'status': 'success',
            'message': 'Successfully updated',
            'data': {
                "product_id": product.product_id,
                "name": product.name,
                "description": product.description,
                "price": product.price
            }
        }
        return response_object, 200


def save_changes(data: Product):
    db.session.add(data)
    db.session.commit()
