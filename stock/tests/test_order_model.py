from django.test import TestCase
from ..models import Order, Transaction, Product

class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample product
        product = Product.objects.create(
            name='Test Product',
            price=10.99,
            quantity=10
        )
        
        # Create a sample transaction
        transaction = Transaction.objects.create(
            product=product,
            quantity=5,
            price=10.99
        )
        
        # Create a sample order
        order = Order.objects.create()
        order.transactions.add(transaction)
    
    def test_order_str(self):
        """
        Test case to verify the __str__ method of the Order model.
        """
        order = Order.objects.get(id=1)
        expected_str = f'{order.created_at}'
        self.assertEqual(str(order), expected_str)
    
    def test_order_transactions(self):
        """
        Test case to verify the transactions associated with an order.
        """
        order = Order.objects.get(id=1)
        transactions = order.transactions.all()
        self.assertEqual(transactions.count(), 1)
    
    def test_complete_transaction(self):
        """
        Test case to verify the complete_transaction method of the Transaction model.
        """
        order = Order.objects.get(id=1)
        transaction = order.transactions.first()
        product = transaction.product
        initial_quantity = product.quantity
        
        transaction.complete_transaction()
        updated_product = Product.objects.get(id=product.id)
        
        self.assertEqual(updated_product.quantity, initial_quantity - transaction.quantity)
    
    def test_reverse_transaction(self):
        """
        Test case to verify the reverse_transaction method of the Transaction model.
        """
        order = Order.objects.get(id=1)
        transaction = order.transactions.first()
        product = transaction.product
        initial_quantity = product.quantity
        
        transaction.reverse_transaction()
        updated_product = Product.objects.get(id=product.id)
        
        self.assertEqual(updated_product.quantity, initial_quantity + transaction.quantity)