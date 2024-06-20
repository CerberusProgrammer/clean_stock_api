from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from ..models import Product

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        Product.objects.create(
            name='Test Product',
            description='This is a test product',
            barcode='1234567890',
            weight=1.5,
            dimension='10x10x10',
            expiration_date='2022-12-31',
            location='Test Location',
            manufacturer=None,
            supplier=None,
            icon='test_icon',
            image=None,
            status=True,
            price=9.99,
            quantity=10,
            quantity_min=5,
            quantity_max=20,
            user=self.user
        )

    def test_name_label(self):
        """
        Test case to verify the label of the 'name' field in the Product model.
        """
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_max_length(self):
        """
        Test case to check the maximum length of the 'description' field in the Product model.
        """
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('description').max_length
        self.assertEqual(max_length, 255)

    def test_quantity_min_blank(self):
        """
        Test case to verify if the 'quantity_min' field of the Product model is blank.

        This test retrieves a Product object with the given id and checks if the 'quantity_min'
        field is set to blank. It asserts that the 'blank' attribute of the field is True.
        """
        product = Product.objects.get(id=1)
        field_blank = product._meta.get_field('quantity_min').blank
        self.assertTrue(field_blank)

    def test_quantity_max_null(self):
        """
        Test case to verify if the 'quantity_max' field of a Product object is set to null.

        This test retrieves a Product object with the specified ID and checks if the 'quantity_max'
        field is set to null. It asserts that the 'null' attribute of the field is True.

        """
        product = Product.objects.get(id=1)
        field_null = product._meta.get_field('quantity_max').null
        self.assertTrue(field_null)

    def test_str_method(self):
        """
        Test the __str__ method of the Product model.

        This test ensures that the __str__ method of the Product model returns the expected string representation.
        It retrieves a product from the database, compares its string representation with the expected value,
        and asserts that they are equal.
        """
        product = Product.objects.get(id=1)
        expected_str = product.name
        self.assertEqual(str(product), expected_str)

    def test_barcode_uniqueness(self):
        """
        Test case to ensure that a ValidationError is raised when creating a product with a duplicate barcode.
        
        (If the barcode is unique a ValidationError will be raised)
        """
        with self.assertRaises(ValidationError):
            Product.objects.create(
                name='Another Test Product',
                description='This is another test product',
                barcode='1234567890',
                price=19.99,
                quantity=20,
                quantity_min=10,
                quantity_max=40
            )

    def test_quantity_within_bounds(self):
        """
        Test case to ensure that the quantity of a product is within the specified bounds.

        This test verifies that the `full_clean()` method of the `Product` model raises a `ValidationError`
        when the quantity is outside the allowed bounds, and does not raise an exception when the quantity
        is within the bounds.

        Steps:
        1. Get a product object with a specific ID.
        2. Set the quantity to a value outside the allowed bounds (30) and assert that a `ValidationError` is raised.
        3. Set the quantity to a value within the allowed bounds (10) and assert that no exception is raised.
        4. Update the minimum quantity allowed for the product to 5.
        5. Set the quantity to a value outside the new allowed bounds (3) and assert that a `ValidationError` is raised.
        6. Set the quantity to a value within the new allowed bounds (10) and assert that no exception is raised.
        """
        product = Product.objects.get(id=1)
        product.quantity = 30
        with self.assertRaises(ValidationError):
            product.full_clean()

        product.quantity = 10
        try:
            product.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

        product.quantity_min = 5
        product.quantity = 3
        with self.assertRaises(ValidationError):
            product.full_clean()

        product.quantity = 10
        try:
            product.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_product_status_toggle(self):
        """
        Test case to verify the toggling of product status.

        This test case retrieves a product from the database, verifies that its status is initially True,
        toggles the status to False, saves the product, and then verifies that the status is now False.
        """
        product = Product.objects.get(id=1)
        self.assertTrue(product.status)

        product.status = False
        product.save()
        self.assertFalse(product.status)