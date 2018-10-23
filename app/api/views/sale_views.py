from flask_restful import Resource, reqparse, marshal, fields
from models import sales
from datetime import datetime

sales = sales.Sales


class SalesAPI(Resource):
    def __init__(self):

        self.parse = reqparse.RequestParser()
        self.parse.add_argument('attendant', type=str,
                                required=True,
                                help="A sale need's an attendant",
                                location='json')

        # Customer details
        self.parse.add_argument('name', type=str,
                                default='Anonymous',
                                location='json')

        self.parse.add_argument('address', type=str,
                                default='Unknown',
                                location='json')

        self.parse.add_argument('contact', type=list,
                                default=['phone', 'email'],
                                location='json')

        # transaction details

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

        self.parse.add_argument('gifts', type=int,
                                default='0',
                                location='json')

        self.parse.add_argument('price', type=int, required=True,
                                help="""You sure are not giving it away for free
                                """,
                                location='json')

        self.parse.add_argument('description', type=str,
                                default='',
                                location='json')

        super(SalesAPI, self).__init__()

    def get(self):
        return {
            'sales': [marshal(sale, sales.sale_fields) for sale in sales.sales]
        }

    def post(self):
        elements = self.parse.parse_args()

        sale = {
            'sales_record': sales[-1]['sales_record'] + 1,
            'attendant': elements['attendant'],
            'name': elements['name'],
            'address': elements['address'],
            'contact': elements['contact'],
            'product': elements['product'],
            'quantity': elements['quantity'],
            'date': datetime.now(),
            'description': elements['description'],
            'transaction_type': elements['transaction_type'],
            'complete': False,
            'gifts': 0,
            'price': elements['price']
        }

        # Find total cost of sale
        sale.update(
            {
                'total': sale.get('quantity') *
                sale.get('price') -
                sale.get('gifts')
            }
        )

        # Add new sale to sales record
        sales.append(sale)

        return {
            'sale': marshal(sale, sale_fields)
        }, 201


sale_fields = {
    'sales_uri': fields.Url('sale'),
    'attendant': fields.String,
    'gifts': fields.Integer,
    'price': fields.Integer,
    'total': fields.Integer
}

"""
    Output nested customer details
                                    """
sale_fields['customer'] = {}
sale_fields['customer']['Name'] = fields.String(attribute='name')
sale_fields['customer']['Address'] = fields.String(attribute='address')

# Create list for customer contacts
sale_fields['customer']['Contact'] = fields.List(
    fields.String, attribute='contact'
)


"""
    Nest the transaction info
                                    """

sale_fields['transaction_info'] = {}

sale_fields['transaction_info']['Product'] = fields.String(attribute='product')
sale_fields['transaction_info']['Quantity'] = fields.Integer(
    attribute='quantity'
)
sale_fields['transaction_info']['Date'] = fields.DateTime(
    attribute='date', dt_format='rfc822'
)
sale_fields['transaction_info']['Description'] = fields.String(
    attribute='description'
)
sale_fields['transaction_info']['Transaction_type'] = fields.String(
    attribute='transaction_type'
)
sale_fields['transaction_info']['Complete'] = fields.Boolean(
    attribute='complete'
)
