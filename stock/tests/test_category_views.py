from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from stock.models import Category

class CategoryViewSetTest(TestCase):
    def setUp(self):
        """
        Set up the necessary objects and data for the test case.

        This method is called before each test method is executed.

        It performs the following steps:
        1. Creates a test user with the username 'testuser' and password 'testpass'.
        2. Creates a test category with the name 'Test Category' and associated with the test user.
        3. Sends a POST request to the '/api/login/' endpoint with the test user's credentials to obtain a token.
        4. Stores the token in the 'token' attribute for later use in the test case.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Test Category', user=self.user)
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['token']

    def test_get_category(self):
        """
        Test case for retrieving a category using GET request.
        """
        response = self.client.get(f'/api/categories/{self.category.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_create_category(self):
        """
        Test case for creating a new category.
        """
        data = {
            'name': 'New Category',
        }
        response = self.client.post('/api/categories/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(id=response.data['id']).name, 'New Category')

    def test_update_category(self):
        """
        Test case for updating a category.
        """
        data = {
            'name': 'Updated Category',
        }
        response = self.client.patch(f'/api/categories/{self.category.id}/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_post_category_duplicate_name(self):
        data = {
            'name': 'Test Category',
        }
        response = self.client.post('/api/categories/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 1)
    
    def test_post_category_duplicate_name_different_user(self):
        # Create a new user
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        response = self.client.post('/api/login/', {'username': 'testuser2', 'password': 'testpass2'})
        token2 = response.data['token']

        # Try to create a new category with the same name as an existing category
        data = {
            'name': 'Test Category',
        }
        response = self.client.post('/api/categories/', data, content_type='application/json', HTTP_AUTHORIZATION='Token ' + token2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_delete_category(self):
        """
        Test case for deleting a category.
        """
        response = self.client.delete(f'/api/categories/{self.category.id}/', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)