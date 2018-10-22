
import unittest
from app import app
import mock
from base64 import b64encode
import json
import sys
from random import randint

my_app = app.my_app


class BasicSaleTests(unittest.TestCase):
    def setUp(self):
        my_app.testing = True
        self.app = my_app.test_client()
        self.path = '/stman/api/v1.0/sales'
        self.headers = {            # User credentials to test
            'Authorization': 'Basic %s' % b64encode(
                b"manager:man").decode("ascii")

        }
        self.response_get = self.app.get(self.path,
                                         headers=self.headers,
                                         follow_redirects=True
                                         )

        # Url Path to individual sale resource
        self.single_sale_path = self.path + '/' + str(1)
        self.response_single_sale = self.app.get(self.single_sale_path,
                                                 headers=self.headers,
                                                 follow_redirects=True
                                                 )

    def test_start_authorization_without_credentials(self):
        response = self.app.get(self.path, follow_redirects=True)
        self.assertEqual(response.status_code, 403,
                         "Grants unauthorized access"
                         )

    def test_call_for_AllSalesAPI(self):
        # Generate url for resourse directly # context unavailable

        resrce = app.AllSalesAPI()

        self.assertRaises(RuntimeError, resrce.get), "Calls non-creatable url"

    def test_true_authorization_for_verified_user(self):
        # Test for access using valid credentials

        self.assertEqual(self.response_get.status_code, 200,
                         "Denies verified user access"
                         )

    def test_get_sales(self):
        # check data request comes in a dictionary

        response_unpack = json.loads(
            self.response_get.get_data().decode(sys.getdefaultencoding())
        )

        self.assertTrue(isinstance(response_unpack, dict),
                        msg="Records not received back as dict")

    def test_fielding_of_ouputs(self):
        # Check if sale record is given back as a nested response

        response_unpack = json.loads(
            self.response_get.get_data().decode(sys.getdefaultencoding())
        )

        self.assertFalse(app.sales is response_unpack['sales'],
                         msg="Sale record details not organised in groups"
                         )

    def test_post_sale(self):
        """
        Verify the passed arguments create new details
        for the new sale.
        """

        response_post_sale = self.app.post(self.path,
                                           headers=self.headers,
                                           data=json.dumps(dict(
                                               attendant='Call me A',
                                               price=354,
                                               product='Baby Soap')),
                                           content_type='application/json',
                                           follow_redirects=True
                                           )
        response_unpack = json.loads(
            response_post_sale.get_data().decode(sys.getdefaultencoding())
        )

        self.assertEqual(response_unpack['sale']['price'], 354,
                         "Sale not created with given data")

    def test_post_sale_arguments(self):
        """
        Verify required arguments are passed for
        resource to be created.
        """

        response_post_sale = self.app.post(self.path,
                                           headers=self.headers,
                                           data=json.dumps(dict(
                                               attend='Call me A',
                                               price=354,
                                               product='Baby Soap')),
                                           content_type='application/json',
                                           follow_redirects=True
                                           )
        response_unpack = json.loads(
            response_post_sale.get_data().decode(sys.getdefaultencoding())
        )
        fail_resp = {'attendant': "A sale need's an attendant"}

        self.assertDictEqual(fail_resp, response_unpack['message'],
                             msg="Fails to request \
                             user for required arguments")

    def test_make_correct_post_sale(self):
        """
        Verify that, with correct arguments,
        a sale record is created
        """

        response_post_sale = self.app.post(self.path,
                                           headers=self.headers,
                                           data=json.dumps(dict(
                                               attendant='Her Again',
                                               price=354,
                                               product='Baby Soap')),
                                           content_type='application/json',
                                           follow_redirects=True
                                           )

        self.assertTrue(response_post_sale.status_code is 201,
                        msg="Fails to create new sale record")

    def test_post_sale_forbidden_arguments(self):
        """
        Verify that unknown data arguments do not create new details
        for the new sale.
        """

        response_post_sale = self.app.post(self.path,
                                           headers=self.headers,
                                           data=json.dumps(dict(
                                               attendant='Somebody I know',
                                               price=354,
                                               product='Baby Soap',
                                               missing_detail='absent')),
                                           content_type='application/json',
                                           follow_redirects=True
                                           )
        response_unpack = json.loads(
            response_post_sale.get_data().decode(sys.getdefaultencoding())
        )

        self.assertRaises(KeyError, lambda: response_unpack[
            'sale']['missing_detail']),
        "Failed to ignore unrequired sale arguments"

    def test_post_sale_that_will_exists(self):
        """
        Verify that the created is a brand new uri.
                            #actually do this ******************************
        Created sale is added to the existing sales.
        """

        response_post_sale = self.app.post(self.path,
                                           headers=self.headers,
                                           data=json.dumps(dict(
                                               attendant='Call me A',
                                               price=354,
                                               product='Baby Soap')),
                                           content_type='application/json',
                                           follow_redirects=True
                                           )
        response_unpack_post = json.loads(
            response_post_sale.get_data().decode(sys.getdefaultencoding())
        )

        # GET Request from all-sales uri
        response_unpack_get = json.loads(
            self.response_get.get_data().decode(sys.getdefaultencoding())
        )

        # Uri for this sale
        new_sale_uri = int(response_unpack_post['sale']['sales_uri'][-1])

        # Uri for last sale
        last_sale_uri = int(
            response_unpack_get[
                'sales'][-1]['sales_uri'][-1]) + 1

        self.assertEqual(new_sale_uri, last_sale_uri,
                         msg="Fails to add new sale to existing sales")

    def test_put_for_AllSales(self):
        """
        Our subclass Resource for 'sales' has no put method.
        Check that changing of this resouce does not work
        """
        how_flask_says_it = "The method is not allowed for the requested URL."
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

        self.assertEqual(response_unpack['message'], how_flask_says_it)


class BasicSingleSaleTest(BasicSaleTests):
    def test_post_sale_that_will_exists(self):
        pass  # Interferes with working of super

    def test_randomized_uri(self):
        guessed_path = self.path + '/' + str(randint(2345, 998888))
        response = self.app.get(guessed_path,
                                headers=self.headers,
                                follow_redirects=True
                                )

        self.assertTrue(response.status_code == 404,
                        msg="Failed to return error for nonexistent url"
                        )

    def test_sale_uri(self):
        """
        Check that the Sale url element is added from the path
        that leads to that sale.
        """

        response_unpack = json.loads(
            self.response_single_sale.get_data().
            decode(sys.getdefaultencoding())
        )

        self.assertEqual(response_unpack['sale']['sales_uri'],
                         self.single_sale_path)

    def test_sale_response_type(self):
        # Response given as dict

        response_unpack = json.loads(
            self.response_single_sale.get_data().
            decode(sys.getdefaultencoding())
        )

        self.assertTrue(isinstance(response_unpack, dict))

    def test_put_sale(self):
        """
        Verify a resource can be updated
        """
        resput_single_sale = self.app.put(self.single_sale_path,
                                          headers=self.headers,
                                          data=json.dumps(dict(
                                              this=1,
                                              sale=2,
                                              fails=3)),
                                          content_type='application/json',
                                          follow_redirects=True
                                          )
        success = 200
        """ response_unpack = json.loads(
            resput_single_sale.get_data().
            decode(sys.getdefaultencoding())
        ) """
        self.assertEqual(resput_single_sale.status_code, success)

    def test_put_sale_with_wrong_url(self):
        """
        Verify a resource can be updated
        """
        path = self.path + '/' + '664'
        resput_single_sale = self.app.put(path,
                                          headers=self.headers,
                                          data=json.dumps(dict(
                                              this=1,
                                              sale=2,
                                              fails=3)),
                                          follow_redirects=True
                                          )
        missing = 404
        """ response_unpack = json.loads(
            resput_single_sale.get_data().
            decode(sys.getdefaultencoding())
        ) """
        self.assertEqual(resput_single_sale.status_code, missing)

    def test_delete_sale(self):

        # Try not remove 'path/../../1', I think every test around wants her
        rm_path = self.path + '/' + '2'
        resdel_sale = self.app.delete(rm_path,
                                      headers=self.headers,
                                      follow_redirects=True
                                      )
        response_unpack = json.loads(
            resdel_sale.get_data().
            decode(sys.getdefaultencoding())
        )
        resdel_sale = self.app.get(rm_path,
                                   headers=self.headers,
                                   follow_redirects=True
                                   )
        # Assert delete
        self.assertDictEqual(response_unpack, {"Effect": True},
                             msg="Failed to delete sale"
                             )

        # Assert sale is discarded
        self.assertEqual(resdel_sale.status_code, 404,
                         msg="Failed to remove deleted item from records"
                         )

    def test_delete_for_missing_resource(self):
        guessed_path = self.path + '/' + str(randint(2345, 998888))
        response = self.app.get(guessed_path,
                                headers=self.headers,
                                follow_redirects=True
                                )

        self.assertFalse(response.status_code == 200,
                         msg="Deletes a nonexistent sale"
                         )


if __name__ == '__main__':
    unittest.main()
