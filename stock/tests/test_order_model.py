from django.test import TestCase
from ..models import Order, Transaction, Product
from django.contrib.auth.models import User

class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
        product = Product.objects.create(
            name='Test Product',
            price=10.99,
            quantity=10,
            user=cls.user
        )
        
        transaction = Transaction.objects.create(
            product=product,
            quantity=5,
            price=10.99,
            user=cls.user
        )
        
        order = Order.objects.create(
            user=cls.user
        )
        order.transactions.add(transaction)
    
    def test_order_transactions(self):
        """
        Test case to verify the transactions associated with an order.
        """
        order = Order.objects.get(id=1)
        transactions = order.transactions.all()
        self.assertEqual(transactions.count(), 1)