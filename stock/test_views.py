from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from stock.models import Order, Transaction, Product

class OrderViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='testuser', password='testpass')
        cls.test_order = Order.objects.create(user=cls.test_user, date=timezone.now())
        cls.test_product = Product.objects.create(user=cls.test_user, name='Test Product', price=10.00, quantity=5)
        cls.test_transaction = Transaction.objects.create(order=cls.test_order, product=cls.test_product, quantity=2, price=20.00)

    def test_fast_report(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/orders/fast-report/')
        self.assertEqual(response.status_code, 200)
        report = response.json()
        self.assertEqual(report['total_ganado'], 40.00)
        self.assertEqual(report['total_transacciones'], 2)
        self.assertEqual(report['promedio_transacciones_diarias'], 0.2857142857142857)
        self.assertEqual(len(report['ventas_ultima_semana']), 1)
        self.assertEqual(report['ventas_ultima_semana'][0]['order_id'], self.test_order.id)
        self.assertEqual(report['ventas_ultima_semana'][0]['date'], self.test_order.created_at)
        self.assertEqual(len(report['ventas_ultima_semana'][0]['transactions']), 1)
        self.assertEqual(report['ventas_ultima_semana'][0]['transactions'][0]['product__name'], self.test_product.name)
        self.assertEqual(report['ventas_ultima_semana'][0]['transactions'][0]['quantity'], self.test_transaction.quantity)
        self.assertEqual(report['ventas_ultima_semana'][0]['transactions'][0]['price'], self.test_transaction.price)