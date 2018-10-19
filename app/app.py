
from flask import Flask, abort

my_app = Flask(__name__, static_url_path="")

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
        'quantity': u'1',
        'date': datetime(2018, 6, 6, 5, 28, 56, 243),
        'description': u'Hot with extra extra spam',
        'transaction_type': u'Cash on Delivery',
        'complete': False,

        'gifts': 1,  # Anything to reduce sale e.g discounts
        'total': 276
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
        'quantity': u'1',
        'date': datetime(2018, 3, 16, 10, 3, 10, 7345),
        'description': u'Black with red eatable margins',
        'transaction_type': u'Credit',
        'complete': False,

        'gifts': 0,  # Any reduction in sale price
        'total': 355
    }

]

sale_fields = {
    'sales_uri': fields.Url('sale'),
    'attendant': fields.String,
    'gifts': fields.Integer,
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
sale_fields['transaction_info']['Quantity'] = fields.String(
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
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('attendant', type=str,
                                required=True,
                                help="A sale need's an attendant",
                                location='json')

        self.parse.add_argument('customer', type=dict,
                                default={
                                    'name': 'Anonymous',
                                    'address': 'unknown',
                                    'contact': 'not stated'
                                },
                                location='json')

        self.parse.add_argument('product', type=str,
                                required=True,
                                help="A product to sell sure has a name",
                                location='json')

        self.parse.add_argument('quantity', type=int,
                                help="How many items", default=1,
                                location='json')

        super(AllSalesAPI, self).__init__()

    def get(self):
        return {
            'sales': [marshal(sale, sale_fields) for sale in sales]
        }



api.add_resource(AllSalesAPI, '/stman/api/v1.0/sales', endpoint='sales')

if __name__ == '__main__':
    my_app.run(debug=True)
