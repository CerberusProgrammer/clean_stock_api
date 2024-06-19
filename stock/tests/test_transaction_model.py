from decimal import Decimal
from django.test import TestCase
from ..models import Transaction, Product

class TransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = Product.objects.create(
            name='Test Product',
            price=10.99,
            quantity=10
        )
        Transaction.objects.create(
            product=product,
            quantity=5,
            price=10.99
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
    
    def test_complete_transaction(self):
        """
        Test case to verify the complete_transaction method of the Transaction model.
        """
        transaction = Transaction.objects.get(id=1)
        transaction.complete_transaction()
        product = Product.objects.get(id=transaction.product.id)
        self.assertEqual(product.quantity, 5)
    
    def test_reverse_transaction(self):
        """
        Test case to verify the reverse_transaction method of the Transaction model.
        """
        transaction = Transaction.objects.get(id=1)
        transaction.reverse_transaction()
        product = Product.objects.get(id=transaction.product.id)
        self.assertEqual(product.quantity, 10)