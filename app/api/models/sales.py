from datetime import datetime

sales = []

# example of a sale record

sale_example = {
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
}


class Sales():
    @staticmethod
    def salesList():
        sales.append(sale_example)

        return sales
