from flask_restful import Resource, reqparse, abort, fields, marshal_with
import datetime
from app.api.v1.models.sales import Sales


class InitializeRecord:
    record = 0

    def __init__(self):
        self.sale_records = {}

    def post_record(self, sale_):
        InitializeRecord.record += 1
        sale_.id = InitializeRecord.record
        self.sale_records[InitializeRecord.record] = sale_

    def fetch_record(self, id):

        return {
            'sale': self.sale_records[id]
        }


sale_instance = InitializeRecord()

sale_fields = {
    'attendant': fields.String,
    'sale_record': fields.Integer,
    'customer_name': fields.Integer,
    'product': fields.String,
    'quantity': fields.Integer,
    'date': fields.DateTime,
    'transaction_type': fields.String,
    'price': fields.Integer,
}


class SaleAPI(Resource):
    @staticmethod
    def verify_existence(sale_id):
        if sale_id not in sale_instance.sale_records:
            error_msg = f'Sale {sale_id} unknown. Maybe create it?'

            abort(404, message=error_msg)

    @marshal_with(sale_fields)
    def get(self, id):
        self.verify_existence(id)

        return sale_instance.fetch_record(id)


class SalesList(Resource):
    @marshal_with(sale_fields)
    def get(self):
        all = [sale for sale
               in sale_instance.sale_records.values()]

        return all

    @marshal_with(sale_fields)
    def post(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('attendant', type=validate,
                                required=True,
                                help="A sale need's an attendant",
                                location='json')

        # Customer details
        self.parse.add_argument('customer_name', type=str,
                                default='Anonymous',
                                location='json')

        self.parse.add_argument('product', type=str,
                                required=True,
                                help="A product to sell sure has a name",
                                location='json')

        self.parse.add_argument('quantity', type=int,
                                help="How many items", default=1,
                                location='json')

        self.parse.add_argument('transaction_type', type=str,
                                default='Cash on Delivery',
                                location='json')

        self.parse.add_argument('price', type=int, required=True,
                                help="""You sure are not giving it away for free
                                """,
                                location='json')

        elements = self.parse.parse_args()

        new_sale = Sales(
            product=elements['product'],
            customer_name=elements['customer_name'],
            price=elements['price'],
            quantity=elements['quantity'],
            transaction_type=elements['transaction_type'],
            attendant=elements['attendant'],
            date=datetime.datetime.now()
        )
        sale_instance.post_record(new_sale)

        return new_sale, 201


def validate(detail, entry):
    if not entry:
        raise ValueError(
            f"Oops! {input} is empty.\nPlease enter be a String")
    if isinstance(detail, int):
        raise ValueError(
            f"Incorrect Detail {element}.\n{detail} should be a String")
