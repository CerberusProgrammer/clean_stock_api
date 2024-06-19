from django.test import TestCase
from ..models import Supplier

class SupplierModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Supplier.objects.create(
            name='Test Supplier',
            icon='test_icon',
            description='This is a test supplier',
            address='Test Address',
            website='http://www.test.com',
            contact_email='test@test.com',
            contact_phone='1234567890',
            country='Test Country',
            city='Test City',
            status=True
        )
    
    def test_name_label(self):
        """
        Test case to verify the label of the 'name' field in the Supplier model.
        """
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_description_blank(self):
        """
        Test case to verify if the 'description' field of the Supplier model is blank.

        This test retrieves a Supplier object with the given id and checks if the 'description'
        field is set to blank. It asserts that the 'blank' attribute of the field is True.
        """
        supplier = Supplier.objects.get(id=1)
        field_blank = supplier._meta.get_field('description').blank
        self.assertTrue(field_blank)
    
    def test_website_max_length(self):
        """
        Test case to check the maximum length of the 'website' field in the Supplier model.
        """
        supplier = Supplier.objects.get(id=1)
        max_length = supplier._meta.get_field('website').max_length
        self.assertEqual(max_length, 100)
    
    def test_status_default_value(self):
        """
        Test case to verify the default value of the 'status' field in the Supplier model.
        """
        supplier = Supplier.objects.get(id=1)
        field_default = supplier._meta.get_field('status').default
        self.assertTrue(field_default)