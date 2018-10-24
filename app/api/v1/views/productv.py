from flask import abort
from flask_restful import Resource, reqparse, fields, marshal_with
import datetime
from app.api.models.products import Products


class IntitalizeRecord:
    record = 0

    def __init__(self):
        self.product_records = {}

    def post_record(self, item):
        IntitalizeRecord.record += 1
        item.id = IntitalizeRecord.record
        self.product_records[IntitalizeRecord.record] = item


class ProductCheck(Resource):
    @staticmethod
    def verify_existence(product_id):
        if product_id not in IntitalizeRecord.product_records:
            reply = f'Product {product_id} unknown. Maybe create it?'

            return {
                'message': reply}


class ProductList(Resource):
    @marshal_with(product_fields)
    def get(self):
        all = [product for product
               in IntitalizeRecord.product_records.values()]

        return all

    @marshal_with(product_fields)
    def post(self):
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

        self.parse.add_argument('in_stock', type=int,
                                default=True,
                                location='json'
                                )

        elements = self.parse.parse_args()

        product = Products(
            'title'=elements['title'],
            'category'=elements['category'],
            'price'=elements['price'],
            'in stock'=elements['in_stock'],
            'date received'=datetime.datetime.now()
        )

        IntitalizeRecord.post_record(product)

        return {
            'product': product
        }, 201


product_fields = {
    'title': fields.String,
    'category': fields.String,
    'price': fields.Integer,
    'in_stock': fields.Integer,
    'date_received': fields.DateTime,
    'id': fields.Integer
}
