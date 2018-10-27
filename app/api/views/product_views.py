from flask_restful import Resource, reqparse, marshal, fields
from app.api.models import products
from datetime import datetime
from flask import abort

products = products.Products.productsList()


class ProductsAPI(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('title', type=str, required=True,
                                help="Please add a title",
                                location='json'
                                )

        self.parse.add_argument('category', type=str,
                                default='None',
                                location='json'
                                )

        self.parse.add_argument('price', type=int,
                                required=True,
                                help="You are not \
                                    allowed to give out stuff for free",
                                location='json'
                                )

        self.parse.add_argument('in stock', type=bool,
                                default=True,
                                location='json'
                                )

        super(ProductsAPI, self).__init__()

    def get(self):
        return {
            'product': [marshal(product, product_fields)
                        for product in products]
        }

    def post(self):
        elements = self.parse.parse_args()

        product = {
            'title': elements['title'],
            'category': elements['category'],
            'price': elements['price'],
            'in stock': True,
            'date received': datetime.now(),
            'id': products[-1]['id'] + 1
        }

        products.append(product)

        return {
            'product': marshal(product, product_fields)
        }, 201


class ProductAPI(Resource):
    """docstring for ProductAPI"""
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('title', type=str,
                                location='json'
                                )

        self.parse.add_argument('category', type=str,
                                location='json'
                                )

        self.parse.add_argument('price', type=int,
                                location='json'
                                )

        self.parse.add_argument('in stock', type=bool,
                                location='json'
                                )

        super(ProductAPI, self).__init__()

    def get(self, id):
        product = [product for product in
                   products if product['id'] is id]

        if not product:
            abort(404)

        return {
            'product': marshal(product[0], product_fields)
        }

    def put(self, id):
        product = [product for product in
                   products if product['id'] is id]

        if not product:
            abort(404)
        elements = self.parse.parse_args()

        for key, value in list(elements.items()):
            if value:
                product[0][key] = value

        return {
            'product': marshal(product, product_fields)
        }

    def delete(self, id):
        product = [product for product
                   in products if product['id'] is id]

        if not product:
            abort(404)
        products.remove(product[0])

        return {
            'Status': True
        }


product_fields = {
    'title': fields.String,
    'category': fields.String,
    'price': fields.Integer,
    'in stock': fields.Boolean,
    'date received': fields.DateTime,
    'url': fields.Url('product')  # Ensure user doen't
                                  # need to know how to generate url
}