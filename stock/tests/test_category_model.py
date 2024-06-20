from django.test import TestCase
from ..models import Category
from django.contrib.auth.models import User

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        Category.objects.create(
            name='Test Category',
            icon='test_icon',
            description='This is a test category',
            status=True,
            user=self.user
        )
    
    def test_name_label(self):
        """
        Test case to verify the label of the 'name' field in the Category model.
        """
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_icon_blank(self):
        """
        Test case to verify if the 'icon' field of the Category model is blank.

        This test retrieves a Category object with the given id and checks if the 'icon'
        field is set to blank. It asserts that the 'blank' attribute of the field is True.
        """
        category = Category.objects.get(id=1)
        field_blank = category._meta.get_field('icon').blank
        self.assertTrue(field_blank)
    
    def test_description_max_length(self):
        """
        Test case to check the maximum length of the 'description' field in the Category model.
        """
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('description').max_length
        self.assertEqual(max_length, 255)
    
    def test_status_default_value(self):
        """
        Test case to verify the default value of the 'status' field in the Category model.
        """
        category = Category.objects.get(id=1)
        field_default = category._meta.get_field('status').default
        self.assertTrue(field_default)