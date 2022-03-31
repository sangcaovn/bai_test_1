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
    @api.expect(_product, validate=True)
    @api.response(201, 'Product successfully created.')
    @api.doc('create a new product')
    def post(self):
        """Creates a new Product """
        data = request.json
        return save_new_product(data=data)


