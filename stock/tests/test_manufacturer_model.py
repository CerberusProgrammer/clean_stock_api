from django.test import TestCase
from ..models import Manufacturer
from django.contrib.auth.models import User

class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        Manufacturer.objects.create(
            name='Test Manufacturer',
            icon='test_icon',
            description='This is a test manufacturer',
            address='Test Address',
            website='http://www.test.com',
            contact_email='test@test.com',
            contact_phone='1234567890',
            country='Test Country',
            city='Test City',
            status=True,
            user = self.user
        )
    
    def test_name_label(self):
        """
        Test case to verify the label of the 'name' field in the Manufacturer model.
        """
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_description_blank(self):
        """
        Test case to verify if the 'description' field of the Manufacturer model is blank.

        This test retrieves a Manufacturer object with the given id and checks if the 'description'
        field is set to blank. It asserts that the 'blank' attribute of the field is True.
        """
        manufacturer = Manufacturer.objects.get(id=1)
        field_blank = manufacturer._meta.get_field('description').blank
        self.assertTrue(field_blank)
    
    def test_website_max_length(self):
        """
        Test case to check the maximum length of the 'website' field in the Manufacturer model.
        """
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field('website').max_length
        self.assertEqual(max_length, 100)
    
    def test_status_default_value(self):
        """
        Test case to verify the default value of the 'status' field in the Manufacturer model.
        """
        manufacturer = Manufacturer.objects.get(id=1)
        field_default = manufacturer._meta.get_field('status').default
        self.assertTrue(field_default)