from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from stock.models import Manufacturer

class ManufacturerViewSetTest(TestCase):
    def setUp(self):
        """
        Set up the necessary objects and data for the test case.

        This method is called before each test method is executed.

        It performs the following steps:
        1. Creates a test user with the username 'testuser' and password 'testpass'.
        2. Creates a test manufacturer with the name 'Test Manufacturer' and associated with the test user.
        3. Sends a POST request to the '/api/login/' endpoint with the test user's credentials to obtain a token.
        4. Stores the token in the 'token' attribute for later use in the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.manufacturer = Manufacturer.objects.create(name='Test Manufacturer', user=self.user)
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['token']

    def test_get_manufacturer(self):
        """
        Test case for retrieving a manufacturer using GET request.
        """
        response = self.client.get(f'/api/manufacturers/{self.manufacturer.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Manufacturer')

    def test_create_manufacturer(self):
        """
        Test case for creating a new manufacturer.
        """
        data = {
            'name': 'New Manufacturer',
        }
        response = self.client.post('/api/manufacturers/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Manufacturer.objects.count(), 2)
        self.assertEqual(Manufacturer.objects.get(id=response.data['id']).name, 'New Manufacturer')

    def test_update_manufacturer(self):
        """
        Test case for updating a manufacturer.
        """
        data = {
            'name': 'Updated Manufacturer',
        }
        response = self.client.patch(f'/api/manufacturers/{self.manufacturer.id}/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, 'Updated Manufacturer')

    def test_delete_manufacturer(self):
        """
        Test case for deleting a manufacturer.
        """
        response = self.client.delete(f'/api/manufacturers/{self.manufacturer.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Manufacturer.objects.count(), 0)
    
    def test_create_duplicate_manufacturer_same_user(self):
        """
        Test case for creating a manufacturer with the same name by the same user.
        """
        data = {
            'name': 'Existing Manufacturer',
        }
        self.client.post('/api/manufacturers/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/api/manufacturers/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_manufacturer_different_users(self):
        """
        Test case for creating a manufacturer with the same name by different users.
        """
        data = {
            'name': 'Existing Manufacturer',
        }
        self.client.post('/api/manufacturers/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        
        self.user2 = User.objects.create_user(username='username2', password='password2')
        response = self.client.post('/api/login/', {'username': 'username2', 'password': 'password2'}, format='json')
        self.token2 = response.data['token']
        
        response = self.client.post('/api/manufacturers/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)