from datetime import datetime


products = []

product_record_example = {
    'title': 'Innocent Coconut Water',
    'category': 'Women sure can Sleep',
    'price': 94534,
    'in stock': True,
    'date received': datetime(
        2018, 5, 30, 22, 12, 38, 649),
    'id': 2
}


class Products(object):
    @staticmethod
    def productsList():
        products.append(product_record_example)

        return products
