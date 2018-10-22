import unittest
from app import app
import mock
from base64 import b64encode
import json
import sys
from random import randint

my_app = app.my_app


class BasicProductTests(unittest.TestCase):
    def setUp(self):
        my_app.testing = True
        self.app = my_app.test_client()
        self.path = '/stman/api/v1.0/products'
        self.headers = {            # User credentials to test
            'Authorization': 'Basic %s' % b64encode(
                b"manager:man").decode("ascii")

        }
        self.single_path = '/stman/api/v1.0/products' + '/' + '1'

        self.response_get = self.app.get(self.path,
                                         follow_redirects=True
                                         )
        self.response_get_auth = self.app.get(self.path,
                                              headers=self.headers,
                                              follow_redirects=True
                                              )
        self.response_get_product = self.app.get(self.single_path,
                                                 headers=self.headers,
                                                 follow_redirects=True
                                                 )

        # Load json data to compare with raw data
        self.response_unpack_get = json.loads(
            self.response_get.get_data().decode(sys.getdefaultencoding())
        )

    def test_access_without_credentials(self):
        """
        Credentials not required not view products
        """
        self.assertNotEqual(self.response_get.status_code, 403,
                            "Failed to show \
                            products without requesting for credentials")

        self.assertNotEqual(self.response_get_auth.status_code, 403,
                            "Failed to show \
                            products without requesting for credentials")

    def test_get_products(self):
        # check data request comes in a dictionary

        response_unpack = json.loads(
            self.response_get.get_data().decode(sys.getdefaultencoding())
        )

        self.assertTrue(isinstance(response_unpack, dict),
                        msg="Failed to output Records in a dictionary")

    def test_get_products_contents(self):
        """
        Product records are lists wrapped in dicts
        """
        self.assertIsInstance(self.response_unpack_get['product'], list,
                              msg="Failed to give record as a list of products"
                              )

    def test_fielding_of_ouputs(self):
        # Check if fields give back data as nested output

        self.assertFalse(app.products is self.response_unpack_get['product'],
                         msg="Failed to group Product record details"
                         )

    def test_access_to_post_products(self):
        """
        Verify that only allowed users(manager) can create product.
        """

        response_post_product = self.app.post(self.path,
                                              follow_redirects=True
                                              )
        self.assertTrue(response_post_product.status_code == 403,
                        msg="Fails to deny\
                        anuthorized user access to create new item")

    def test_post_product(self):
        """
        Verify that necessary arguments are passed for
        needed for product to be created.
        """

        response_post_product = self.app.post(self.path,
                                              headers=self.headers,
                                              data=json.dumps(dict(
                                                  missing_price='Call her A',
                                                  title='Almost Ours',
                                                  category="I'm taking her\
                                                  to coffee")),
                                              content_type='application/json',
                                              follow_redirects=True
                                              )
        response_unpack = json.loads(
            response_post_product.get_data().decode(sys.getdefaultencoding())
        )
        fail_resp = "You are not \
                                    allowed to give out stuff for free"

        self.assertIn(fail_resp, response_unpack['message']['price'],
                      msg="Fails to request \
                             user for required arguments")

    def test_make_sensible_post_for_product(self):
        """
        Verify that a new product can be created.
        """

        response_post_sale = self.app.post(self.path,
                                           headers=self.headers,
                                           data=json.dumps(dict(
                                               title='Loose a Screw',
                                               price=7854,
                                               category="Vodkaless Alcohol")),
                                           content_type='application/json',
                                           follow_redirects=True
                                           )

        self.assertTrue(response_post_sale.status_code is 201,
                        msg="Fails to create new product")

    def test_post_product_using_unknown_details(self):
        """
        Verify that unknown data arguments do not create new details
        for the new sale.
        """

        response_post_sale = self.app.post(self.path,
                                           headers=self.headers,
                                           data=json.dumps(dict(
                                               I_='Somebody I know',
                                               got=354,
                                               drunk='Baby Soap',
                                               a_little='absent')),
                                           content_type='application/json',
                                           follow_redirects=True
                                           )
        response_unpack = json.loads(
            response_post_sale.get_data().decode(sys.getdefaultencoding())
        )

        self.assertRaises(KeyError, lambda: response_unpack[
            'sale']['drunk']),
        "Fails to ignore unknown product details"

    def test_post_product_really_creates_product(self):
        """
        Verify that the created product gets a uri.
        This uri should be added to those of existing products.
        """

        response_post_sale = self.app.post(self.path,
                                           headers=self.headers,
                                           data=json.dumps(dict(
                                               title='Call me A',
                                               price=354,
                                               category='Bubbless Soap')),
                                           content_type='application/json',
                                           follow_redirects=True
                                           )
        response_unpack_post = json.loads(
            response_post_sale.get_data().decode(sys.getdefaultencoding())
        )

        # Request we get from fetch-all-products
        response_unpack_get = json.loads(
            self.response_get.get_data().decode(sys.getdefaultencoding())
        )

        # Uri we created for this product
        product_uri = int(response_unpack_post['product']['url'][-1])

        # Uri we had last
        last_product_known = int(
            response_unpack_get[
                'product'][-1]['url'][-1]) + 1

        self.assertEqual(product_uri, last_product_known,
                         msg="Fails to add new sale to existing sales")

    def test_put_for_Products(self):
        """
        We are 'not supposed to be able' to add
        data to the Proucts resource.
        'Put' should fail.
        """
        what_we_expect = "The method is not allowed for the requested URL."
        resput_sales = self.app.put(self.path,
                                    headers=self.headers,
                                    data=json.dumps(dict(
                                        this=1,
                                        thing=2,
                                        fails=3)),
                                    follow_redirects=True
                                    )
        response_unpack = json.loads(
            resput_sales.get_data().
            decode(sys.getdefaultencoding())
        )

        self.assertTrue(response_unpack['message'] == what_we_expect,
                        msg="Fails to give \
                        error for use of a nonexistent method")


class BasicSingleProductTests(BasicProductTests):
    def test_guess_path_to_product(self):
        guessed_path = self.path + '/' + str(randint(2345, 998888))
        response = self.app.get(guessed_path,
                                headers=self.headers,
                                follow_redirects=True
                                )

        self.assertTrue(response.status_code == 404,
                        msg="Failed to return\
                        'not found error' for nonexistent url"
                        )

    def test_product_output_uri(self):
        """
        Check that the Product url element is added from the path
        leading to the product.
        """

        response_unpack = json.loads(
            self.response_get_product.get_data().
            decode(sys.getdefaultencoding())
        )

        self.assertEqual(response_unpack['product']['url'],
                         self.single_path)

    def test_delete_for_missing_resource(self):
        guessed_path = self.path + '/' + str(randint(2345, 998888))
        response = self.app.get(guessed_path,
                                headers=self.headers,
                                follow_redirects=True
                                )

        self.assertFalse(response.status_code == 200,
                         msg="Deletes a nonexistent sale"
                         )

    def test_delete_product(self):

        # Try not remove 'path/../../1', I think every test around wants her
        rm_path = self.path + '/' + '2'
        resdel_prod = self.app.delete(rm_path,
                                      headers=self.headers,
                                      follow_redirects=True
                                      )
        response_unpack = json.loads(
            resdel_prod.get_data().
            decode(sys.getdefaultencoding())
        )
        resdel_prod = self.app.get(rm_path,
                                   headers=self.headers,
                                   follow_redirects=True
                                   )
        # Assert delete
        self.assertDictEqual(response_unpack, {"Status": True},
                             msg="Failed to delete sale"
                             )

        # Assert sale is discarded
        self.assertNotEqual(resdel_prod.status_code, 404,
                            msg="Failed to remove deleted item from records"
                            )

    def test_get_product_ouput(self):
        # Product is received wrapped in dict

        response_unpack = json.loads(
            self.response_get_product.get_data().
            decode(sys.getdefaultencoding())
        )

        self.assertTrue(isinstance(response_unpack, dict))

    def test_put_product(self):
        """
        Verify an existing product can be updated
        """
        resput_single_prod = self.app.put(self.single_path,
                                          headers=self.headers,
                                          data=json.dumps(dict(
                                              this=1,
                                              is_=2,
                                              testing=3)),
                                          content_type='application/json',
                                          follow_redirects=True
                                          )
        success = 200
        """ response_unpack = json.loads(
            resput_single_sale.get_data().
            decode(sys.getdefaultencoding())
        ) """
        self.assertEqual(resput_single_prod.status_code, success)

    def test_put_product_using_bad_url(self):
        """
        Verify a resource can be updated
        """
        path = self.path + '/' + '664'
        resput_single_prod = self.app.put(path,
                                          headers=self.headers,
                                          data=json.dumps(dict(
                                              one=1,
                                              two=2,
                                              JUMP=3)),
                                          follow_redirects=True
                                          )
        missing = 404
        self.assertEqual(resput_single_prod.status_code, missing)
