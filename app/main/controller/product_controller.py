from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import ProductDto
from ..service.product_service import save_new_product, get_all_products, get_a_product
from typing import Dict, Tuple

api = ProductDto.api
_product = ProductDto.product


@api.route('/')
class ProductList(Resource):
    @api.doc('list_of_products')
    @admin_token_required
    @api.marshal_list_with(_product, envelope='data')
    def get(self):
        """List all registered products"""
        return get_all_products()

    @api.expect(_product, validate=True)
    @api.response(201, 'Product successfully created.')
    @api.doc('create a new product')
    def post(self):
        """Creates a new Product """
        data = request.json
        return save_new_product(data=data)


@api.route('/<product_id>')
@api.param('id', 'The Product identifier')
@api.response(404, 'Product not found.')
class Product(Resource):
    @api.doc('get a product')
    @api.marshal_with(_product)
    def get(self, id):
        """get a product given its identifier"""
        product = get_a_product(id)
        if not product:
            api.abort(404)
        else:
            return product

