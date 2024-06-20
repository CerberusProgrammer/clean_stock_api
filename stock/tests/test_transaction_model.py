from decimal import Decimal
from django.test import TestCase
from ..models import Transaction, Product
from django.contrib.auth.models import User

class TransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
        product = Product.objects.create(
            name='Test Product',
            price=10.99,
            quantity=10,
            user=cls.user
        )
        Transaction.objects.create(
            product=product,
            quantity=5,
            price=10.99,
            user=cls.user
        )
    
    def test_product_name(self):
        """
        Test case to verify the name of the associated product in the Transaction model.
        """
        transaction = Transaction.objects.get(id=1)
        product_name = transaction.product.name
        self.assertEqual(product_name, 'Test Product')
    
    def test_quantity(self):
        """
        Test case to verify the quantity of the Transaction model.
        """
        transaction = Transaction.objects.get(id=1)
        quantity = transaction.quantity
        self.assertEqual(quantity, 5)
    
    def test_price(self):
        """
        Test case to verify the price of the Transaction model.
        """
        transaction = Transaction.objects.get(id=1)
        price = transaction.price
        self.assertEqual(price, Decimal('10.99'))