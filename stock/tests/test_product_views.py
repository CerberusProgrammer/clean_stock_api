from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from stock.models import Product

class ProductViewSetTest(TestCase):
    def setUp(self):
        """
        Set up the necessary objects and data for the test case.

        This method is called before each test method is executed.

        It performs the following steps:
        1. Creates a test user with the username 'testuser' and password 'testpass'.
        2. Creates a test product with the name 'Test Product', description 'This is a test product',
            price 19.99, barcode '1234567890', and associated with the test user.
        3. Sends a POST request to the '/api/login/' endpoint with the test user's credentials to obtain a token.
        4. Stores the token in the 'token' attribute for later use in the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name='Test Product', description='This is a test product', price=19.99, barcode='1234567890', user=self.user)
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['token']

    def test_get_product(self):
        """
        Test case for retrieving a product using GET request.
        """
        response = self.client.get(f'/api/products/{self.product.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')
    
    def test_patch_product(self):
        """
        Test case for patching a product.
        """
        data = {'name': 'Updated Product'}
        response = self.client.patch(f'/api/products/{self.product.id}/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_delete_product(self):
        """
        Test case for deleting a product.
        """
        response = self.client.delete(f'/api/products/{self.product.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
    
    def test_post_product(self):
        """
        Test case for posting a new product.
        """
        data = {
            'name': 'New Product',
            'description': 'This is a new product',
            'price': 29.99,
            'barcode': '0987654321',
        }
        response = self.client.post('/api/products/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(id=response.data['id']).name, 'New Product')
    
    def test_post_product_duplicate_barcode(self):
        """
        Test case to verify that posting a product with a duplicate barcode returns a 400 BAD REQUEST status code.
        """
        data = {
            'name': 'New Product',
            'description': 'This is a new product',
            'price': 29.99,
            'barcode': self.product.barcode,
        }
        response = self.client.post('/api/products/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 1)
    
    def test_post_product_duplicate_barcode_different_user(self):
        """
        Test case to verify that a product with a duplicate barcode can be created by a different user.
        """
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        response = self.client.post('/api/login/', {'username': 'testuser2', 'password': 'testpass2'})
        token2 = response.data['token']

        data = {
            'name': 'New Product',
            'description': 'This is a new product',
            'price': 29.99,
            'barcode': self.product.barcode,
        }
        response = self.client.post('/api/products/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + token2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)