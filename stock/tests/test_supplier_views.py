from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from stock.models import Supplier

class SupplierViewSetTest(TestCase):
    def setUp(self):
        """
        Set up the necessary objects and data for the test case.

        This method is called before each test method is executed.

        It performs the following steps:
        1. Creates a test user with the username 'testuser' and password 'testpass'.
        2. Creates a test supplier with the name 'Test Supplier' and associated with the test user.
        3. Sends a POST request to the '/api/login/' endpoint with the test user's credentials to obtain a token.
        4. Stores the token in the 'token' attribute for later use in the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.supplier = Supplier.objects.create(name='Test Supplier', user=self.user)
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['token']

    def test_get_supplier(self):
        """
        Test case for retrieving a supplier using GET request.
        """
        response = self.client.get(f'/api/suppliers/{self.supplier.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Supplier')

    def test_create_supplier(self):
        """
        Test case for creating a new supplier.
        """
        data = {
            'name': 'New Supplier',
        }
        response = self.client.post('/api/suppliers/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 2)
        self.assertEqual(Supplier.objects.get(id=response.data['id']).name, 'New Supplier')

    def test_update_supplier(self):
        """
        Test case for updating a supplier.
        """
        data = {
            'name': 'Updated Supplier',
        }
        response = self.client.patch(f'/api/suppliers/{self.supplier.id}/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, 'Updated Supplier')

    def test_delete_supplier(self):
        """
        Test case for deleting a supplier.
        """
        response = self.client.delete(f'/api/suppliers/{self.supplier.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 0)
    
    def test_create_duplicate_supplier_same_user(self):
        """
        Test case for creating a duplicate supplier by the same user.
        """
        supplier_data = {'name': 'Test Supplier'}
        self.client.post('/api/suppliers/', supplier_data, HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/api/suppliers/', supplier_data, HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_supplier_different_user(self):
        """
        Test case for creating a duplicate supplier by a different user.
        """
        supplier_data = {'name': 'Test Supplier'}
        self.client.post('/api/suppliers/', supplier_data, HTTP_AUTHORIZATION='Token ' + self.token)
        
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        response = self.client.post('/api/login/', {'username': 'testuser2', 'password': 'testpass2'})
        token2 = response.data['token']

        response = self.client.post('/api/suppliers/', supplier_data, HTTP_AUTHORIZATION='Token ' + token2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)