from flask_restful import Resource, reqparse, abort, fields, marshal_with
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

    def fetch_record(self, id):

        return {
            'product': self.product_records[id]
        }


product_fields = {
    'title': fields.String,
    'category': fields.String,
    'price': fields.Integer,
    'in_stock': fields.Integer,
    'date_received': fields.DateTime,
    'id': fields.Integer
}

record_instance = IntitalizeRecord()


class ProductAPI(Resource):
    @staticmethod
    def verify_existence(product_id):
        if product_id not in record_instance.product_records:
            reply = f'Product {product_id} unknown. Maybe create it?'

            abort(404, message=reply)

    @marshal_with(product_fields)
    def get(self, id):
        self.verify_existence(id)

        return record_instance.fetch_record(id)


class ProductList(Resource):
    @marshal_with(product_fields)
    def get(self):
        all = [product for product
               in record_instance.product_records.values()]

        return all

    @marshal_with(product_fields)
    def post(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('title', type=validate_inputs, required=True,
                                help="Please add a title",
                                location='json'
                                )

        self.parse.add_argument('category', type=validate_inputs,
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
            title=elements['title'],
            category=elements['category'],
            price=elements['price'],
            in_stock=elements['in_stock'],
            date_received=datetime.datetime.now()
        )

        record_instance.post_record(product)

        return {
            'product': product
        }, 201


def validate_inputs(element, input_arg):
    if not element:
        raise ValueError(
            f"Oops! {input_arg} is empty.\nPlease enter be a String")
    if isinstance(input, int):
        raise ValueError(
            f"Incorrect Detail {element}.\nTry making {input_arg} a String")
    return element
