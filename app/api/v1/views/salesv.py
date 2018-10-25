from flask_restful import Resource, reqparse, abort, fields, marshal_with
import datetime
from app.api.v1.models.sales import sales


class InitializeRecord:
    record = 0

    def __init__(self):
        self.sale_records = {}

    def post_record(self, sale_item):
        InitializeRecord.record += 1
        sale_item.id = InitializeRecord.record
        self.sale_records[InitializeRecord.record] = sale_item

    def fetch_record(self, id):

        return {
            'sale': self.sale_records[id]
        }


sale_instance = InitializeRecord()


class SaleAPI(Resource):
    @staticmethod
    def verify_existence(sale_record):
        if sale_record not in sale_instance.sale_records:
            error_msg = f'Sale {sale_record} unknown. Maybe create it?'

            abort(404, message=error_msg)

    @marshal_with(sale_fields)
    def get(self, sale_record):
        self.verify_existence(sale_record)

        return sale_instance.fetch_record(sale_record)



sale_fields = {
    'attendant': fields.String,
    'customer_name': fields.Integer,
    'product': fields.String,
    'quantity': fields.Integer,
    'date': fields.DateTime,
    'transaction_type': fields.String,
    'price': fields.Integer,
    'total': fields.Integer
}
