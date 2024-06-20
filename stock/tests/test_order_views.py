from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from stock.models import Order, Product, Transaction

class OrderViewSetTest(TestCase):
    def setUp(self):
        """
        Set up the necessary objects and data for the test case.

        This method is called before each test method is executed.

        It performs the following steps:
        1. Creates a test user with the username 'testuser' and password 'testpass'.
        2. Creates a test order associated with the test user.
        3. Sends a POST request to the '/api/login/' endpoint with the test user's credentials to obtain a token.
        4. Stores the token in the 'token' attribute for later use in the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.order = Order.objects.create(user=self.user)
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['token']

    def test_get_order(self):
        """
        Test case for retrieving an order using GET request.
        """
        response = self.client.get(f'/api/orders/{self.order.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_create_order(self):
        """
        Test case for creating a new order.
        """
        product = Product.objects.create(user=self.user, name='Test Product', barcode='xyz', price=10.0, quantity=5)
        transaction = Transaction.objects.create(user=self.user, product=product, price=100.0, quantity=1)

        data = {
            'user': self.user.id,
            'transactions': [transaction.id],
        }
        response = self.client.post('/api/orders/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=response.data['id']).user.id, self.user.id)
    
    def test_create_order_with_same_product(self):
        """
        Test case for creating a new order with 10 transactions of the same product.
        """
        product = Product.objects.create(user=self.user, name='Test Product', price=10.0, barcode='xyz', quantity=50)

        transactions = [Transaction.objects.create(user=self.user, product=product, price=100.0, quantity=1).id for _ in range(10)]

        data = {
            'user': self.user.id,
            'transactions': transactions,
        }
        response = self.client.post('/api/orders/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=response.data['id']).user.id, self.user.id)

    def test_create_order_with_different_products(self):
        """
        Test case for creating a new order with 10 different products per transaction.
        """
        transactions = [Transaction.objects.create(
            user=self.user, 
            product=Product.objects.create(
                user=self.user, 
                name=f'Test Product {i}', 
                barcode=f'xyz{i}',
                price=10.0, 
                quantity=5
            ), 
            price=100.0, 
            quantity=1
        ).id for i in range(10)]

        data = {
            'user': self.user.id,
            'transactions': transactions,
        }

        response = self.client.post('/api/orders/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=response.data['id']).user.id, self.user.id)
    
    def test_update_order(self):
        """
        Test case for updating an order.
        """
        new_transaction = Transaction.objects.create(
            user=self.user, 
            product=Product.objects.create(
                user=self.user, 
                name='Test Product', 
                price=10.0, 
                quantity=5, 
                barcode='new_barcode'
            ), 
            price=100.0, 
            quantity=1
        )

        data = {
            'user': self.user.id,
            'transactions': [new_transaction.id],
        }

        response = self.client.patch(f'/api/orders/{self.order.id}/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.user.id, self.user.id)

    def test_delete_order(self):
        """
        Test case for deleting an order.
        """
        response = self.client.delete(f'/api/orders/{self.order.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
    
    def test_multiple_orders_with_same_transactions(self):
        """
        Test case for creating multiple orders with the same transactions.
        """
        Order.objects.all().delete()

        for i in range(2):
            product = Product.objects.create(user=self.user, name='Test Product', price=10.0, quantity=50, barcode=f'Test Product {i}')

            transactions = [Transaction.objects.create(user=self.user, product=product, price=100.0, quantity=1).id for _ in range(3)]

            data = {
                'user': self.user.id,
                'transactions': transactions,
            }
            response = self.client.post('/api/orders/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.filter(user=self.user).count(), 2)
    
    def test_order_creation_reduces_product_quantity(self):
        """
        Test case for verifying that creating an order reduces the product quantity.
        """
        product = Product.objects.create(user=self.user, name='Test Product', barcode='xyz', price=10.0, quantity=50)
        initial_quantity = product.quantity
        transaction_quantity = 5

        transaction = Transaction.objects.create(user=self.user, product=product, price=product.price, quantity=transaction_quantity)

        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post('/api/orders/', {'transactions': [transaction.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=product.id)

        self.assertEqual(product.quantity, initial_quantity - transaction_quantity)

    def test_order_cancellation_returns_product_quantity(self):
        """
        Test case for verifying that cancelling an order returns the product quantity.
        """
        initial_quantity = 50
        transaction_quantity = 5
        product = Product.objects.create(user=self.user, name='Test Product', price=10.0, quantity=initial_quantity)
        transaction = Transaction.objects.create(user=self.user, product=product, price=100.0, quantity=transaction_quantity)

        data = {
            'user': self.user.id,
            'transactions': [transaction.id],
        }
        response = self.client.post('/api/orders/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        order_id = response.data['id']

        self.client.post(f'/api/orders/{order_id}/cancel/', HTTP_AUTHORIZATION='Token ' + self.token)

        product.refresh_from_db()
        self.assertEqual(product.quantity, initial_quantity)