from typing import Dict, Tuple

from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import ProductDto
from ..service.product_service import create_a_product, get_product_list, get_a_product, update_a_product

api = ProductDto.api
_product = ProductDto.product

@api.route('/')
class ProductList(Resource):
    @api.expect(_product, validate=True)
    @api.response(201, 'Product successfully created.')
    @api.doc('create a product')
    @admin_token_required
    def post(self):
        """Creates a new product """
        data = request.json
        return create_a_product(data=data)
    @api.doc('list_of_product')
    @api.marshal_list_with(_product, envelope='data')
    def get(self):
        """Get product list"""
        return get_product_list()
@api.route('/<name>')
@api.param('name', 'The name of product')
@api.response(404, 'Product not found.')
class Product(Resource):
    @api.doc('get a product')
    @api.marshal_with(_product)
    def get(self, name):
        """get a product"""
        product = get_a_product(name)
        if not product:
            api.abort(404)
        else:
            return product
    @api.doc('update a product')
    @api.marshal_with(_product)
    def patch(self, name):
        """Update a product """
        data = request.json
        return update_a_product(name, data=data)   