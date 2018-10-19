
from flask import Flask, abort
from flask_restful import Api, fields, Resource, reqparse, marshal
from datetime import datetime

my_app = Flask(__name__, static_url_path="")
api = Api(my_app)

sales = [
    {
        'sales_record': 1,
        'attendant': u'Attendant One',

        # Customer contacts
        'name': u'Customer One',
        'address': u'45 bright street',
        'contact': [u'+00012345', u'customer_c@example.co'],

        # Transaction Info
        'product': u'Spam 2.0',
        'quantity': 1,
        'date': datetime(2018, 6, 6, 5, 28, 56, 243),
        'description': u'Hot with extra extra spam',
        'transaction_type': u'Cash on Delivery',
        'complete': False,

        'gifts': 100,  # Anything to reduce sale e.g discounts
        'price': 276,
    },

    {
        'sales_record': 2,
        'attendant': u'Attendant Six',

        # Customer contacts
        'name': u'Customer fifty',
        'address': u'42 bright street',
        'contact': [u'+00012345', u'customer_c@example.co'],

        # Transaction Info
        'product': u'Spam 2.2',
        'quantity': 1,
        'date': datetime(2018, 3, 16, 10, 3, 10, 7345),
        'description': u'Black with red eatable margins',
        'transaction_type': u'Credit',
        'complete': False,

        'gifts': 0,  # Any reduction in sale price
        'price': 355
    }

]

# calculate total cost of sale

for each_sale in sales:
    each_sale.update(
        {
            'total': each_sale.get('quantity') *
            each_sale.get('price') -
            each_sale.get('gifts')
        }
    )

sale_fields = {
    'sales_uri': fields.Url('sale'),
    'attendant': fields.String,
    'gifts': fields.Integer,
    'price': fields.Fixed,
    'total': fields.Fixed
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


class AllSalesAPI(Resource):
    def __init__(self):

        """
        verify arguments' are in correct format
        """

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

        super(AllSalesAPI, self).__init__()

    def get(self):
        return {
            'sales': [marshal(sale, sale_fields) for sale in sales]
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


class SaleAPI(Resource):
    """docstring for SaleAPI"""
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('attendant', type=str, location='json')
        self.parse.add_argument('transaction_info', type=dict, location='json')
        self.parse.add_argument('gifts', type=int, location='json')
        self.parse.add_argument('total',
                                type=float,
                                location='json'
                                )
        super(SaleAPI, self).__init__()

    def get(self, sales_record):
        sale = [sale for sale in sales if sale['sales_record'] == sales_record]

        if not sale:
            abort(404)

        return {'sale': marshal(sale[0], sale_fields)}


api.add_resource(AllSalesAPI, '/stman/api/v1.0/sales', endpoint='sales')
api.add_resource(SaleAPI, '/stman/api/v1.0/sales/<int:sales_record>',
                 endpoint='sale'
                 )

if __name__ == '__main__':
    my_app.run(debug=True)
