import unittest
from run import create_app
import json
import sys
from random import randint

my_app = create_app()


class BasicProductTests(unittest.TestCase):
    def setUp(self):
        my_app.testing = True
        self.app = my_app.test_client()
        self.path = '/api/v1.0/products'
        self.single_path = '/api/v1.0/products' + '/' + '1'
        self.headers = {
            'Authorization': 'Bearer ' + self.give_access()

        }

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

    def give_access(self):
        # Register test user
        self.app.post('api/v1.0/users/register',
                      data=json.dumps(dict(
                          email='evil.cow@c.dairy',
                          password='pa55word',
                          name="Evil Cow")),
                      content_type='application/json',
                      follow_redirects=True

                      )
        # Login test user
        resp = self.app.post('api/v1.0/users/access',
                             data=json.dumps(dict(
                                 email='evil.cow@c.dairy',
                                 password='pa55word',
                                 name="Evil Cow")),
                             content_type='application/json',
                             follow_redirects=True

                             )
        response = json.loads(
            resp.get_data().decode(sys.getdefaultencoding())
        )
        return response['Access Token']

    def test_access_without_credentials(self):
        """
        Credentials not required to view products
        """
        self.assertNotEqual(self.response_get.status_code, 403,
                            "Failed to show \
                            products without requesting for credentials")

    def test_pass_credentials_for_fun(self):
        """
        Passing credentials unnecessary to view products
        """
        self.assertNotEqual(self.response_get_auth.status_code, 403,
                            "Failed to show \
                            products without requesting for credentials")

    def test_get_products(self):
        # check data request comes in a list

        response_unpack = json.loads(
            self.response_get.get_data().decode(sys.getdefaultencoding())
        )

        self.assertTrue(isinstance(response_unpack, list),
                        msg="Failed to output Records in a list")

    def test_get_products_contents(self):
        """
        Product records starts empty
        """
        self.assertRaises(IndexError, lambda: self.response_unpack_get[10],
                          ), "Failes to initialize product record as empty"

    def test_access_to_post_products(self):
        """
        Verify that only only registered user can create product.
        """

        response_post_product = self.app.post(self.path,
                                              follow_redirects=True
                                              )
        self.assertTrue(response_post_product.status_code == 401,
                        msg="Fails to deny\
                        anuthorized user access to create new item")

    def test_post_product(self):
        """
        Verify that necessary arguments are passed for
        for product to be created.
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

    def test_post_product_invalid_name(self):
        """
        Verify that necessary arguments are passed for
        for product to be created.
        """

        response_post_product = self.app.post(self.path,
                                              headers=self.headers,
                                              data=json.dumps(dict(
                                                  price='Call her A',
                                                  title='Almost Ours',
                                                  category="I'm taking her\
                                                  to coffee")),
                                              content_type='application/json',
                                              follow_redirects=True
                                              )
        response_unpack = json.loads(
            response_post_product.get_data().decode(sys.getdefaultencoding())
        )
        print(response_unpack)

        self.assertEqual(400, response_post_product.status_code,
                         msg="Fails to restrict\
                      user to give attendant name to letters")

    def test_post_product_invalid_(self):
        """
        Verify that necessary arguments are passed for
        for product to be created.
        """

        response_post_product = self.app.post(self.path,
                                              headers=self.headers,
                                              data=json.dumps(dict(
                                                  price='Call her A',
                                                  product=54,
                                                  category="I'm taking her\
                                                  to coffee")),
                                              content_type='application/json',
                                              follow_redirects=True
                                              )
        response_unpack = json.loads(
            response_post_product.get_data().decode(sys.getdefaultencoding())
        )
        print(response_unpack)

        self.assertEqual(400, response_post_product.status_code,
                         msg="Fails to restrict\
                      user to give attendant name to letters")

    def test_post_product_using_unknown_details(self):
        """
        Verify that unknown data arguments do not create new details
        for the new product.
        """

        response_post_product = self.app.post(self.path,
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
            response_post_product.get_data().decode(sys.getdefaultencoding())
        )

        self.assertRaises(KeyError, lambda: response_unpack[
            0]['drunk']),
        "Fails to ignore unknown product details"

    def test_post_product_really_creates_product(self):
        """
        Verify that the created product gets a uri.
        This uri should be added to those of existing products.
        """

        response_post_product = self.app.post(self.path,
                                              headers=self.headers,
                                              data=json.dumps(dict(
                                                  title='Call me A',
                                                  price=354,
                                                  category='Bubbless Soap')),
                                              content_type='application/json',
                                              follow_redirects=True
                                              )
        response_unpack_post = json.loads(
            response_post_product.get_data().decode(sys.getdefaultencoding())
        )

        # Uri we created for this product
        product_uri = (response_unpack_post['id'])

        # Fetch all records
        response_get = self.app.get(self.path,
                                    follow_redirects=True
                                    )

        # Request we get from fetch-all-products
        response_unpack_get = json.loads(
            response_get.get_data().decode(sys.getdefaultencoding())
        )

        # Uri we had last
        last_product_known = (
            response_unpack_get[
                -1]['id'])

        self.assertEqual(product_uri, last_product_known,
                         msg="Fails to add new product to existing products")

    def test_put_for_Products(self):
        """
        We are 'not supposed to be able' to add
        data to the Proucts resource.
        'Put' should fail.
        """

        what_we_expect = "The method is not allowed for the requested URL."
        resput_products = self.app.put(self.path,
                                       headers=self.headers,
                                       data=json.dumps(dict(
                                           this=1,
                                           thing=2,
                                           fails=3)),
                                       follow_redirects=True
                                       )
        response_unpack = json.loads(
            resput_products.get_data().
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
        We expect the url number to have increased
        """

        response_post_product = self.app.post(self.path,
                                              headers=self.headers,
                                              data=json.dumps(dict(
                                                  title='Call me A',
                                                  price=354,
                                                  category='Bubbless Soap')),
                                              content_type='application/json',
                                              follow_redirects=True
                                              )
        response_unpack = json.loads(
            response_post_product.get_data().decode(sys.getdefaultencoding())
        )

        self.assertGreaterEqual(response_unpack['id'],
                                int(self.single_path[-1]))

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
        created = 201

        self.assertEqual(resput_single_prod.status_code, created,
                         msg="Fails to edit a product")

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
        self.assertEqual(resput_single_prod.status_code, missing,
                         msg="Failes. Edits a nonexistent product")
