from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Promotion, Product, Category

class PromotionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='testuser', password='testpass')
        cls.test_category = Category.objects.create(user=cls.test_user, name='Test Category')
        cls.test_product = Product.objects.create(
            user=cls.test_user,
            name='Test Product',
            price=10.00,
            barcode='1234567891',
            category=cls.test_category
        )
        cls.test_promotion = Promotion.objects.create(
            user=cls.test_user,
            name='Test Promotion',
            description='This is a test promotion',
            discount_percentage=20.00,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=7),
            status=True
        )
        cls.test_promotion.products.add(cls.test_product)
        cls.test_promotion.categories.add(cls.test_category)
    
    def test_is_active(self):
        """
        Test case to verify the 'is_active' method of the Promotion model.
        """
        promotion = Promotion.objects.get(id=1)
        self.assertTrue(promotion.is_active())
    
    def test_is_not_active(self):
        """
        Test case to verify the 'is_active' method of the Promotion model.
        """
        promotion = Promotion.objects.get(id=1)
        promotion.end_date = timezone.now() - timezone.timedelta(days=1)
        promotion.save()
        self.assertFalse(promotion.is_active())
    
    def test_get_price_with_discount(self):
        """
        Test case to verify the 'get_price_with_discount' method of the Product model.
        """
        product = Product.objects.get(id=1)
        price_with_discount = float(product.get_price_with_discount())
        
        expected_price = float(product.price) - float(product.price) * float(self.test_promotion.discount_percentage / 100)
        self.assertEqual(price_with_discount, expected_price)
    
    def test_get_price_in_product_category(self):
        category = Category.objects.create(user=self.test_user, name="Electronics")

        promotion = Promotion.objects.create(
            discount_percentage=20,
            start_date=timezone.now() - timezone.timedelta(days=7),
            end_date=timezone.now() + timezone.timedelta(days=7),
            user=self.test_user
        )
        promotion.categories.add(category)
        promotion.save()

        products = [
            Product.objects.create(user=self.test_user, barcode="P1", name="Product 1", price=Decimal('100.00'), category=category),
            Product.objects.create(user=self.test_user, barcode="P2", name="Product 2", price=Decimal('200.00'), category=category),
            Product.objects.create(user=self.test_user, barcode="P3", name="Product 3", price=Decimal('300.00'), category=category),
        ]

        for product in products:
            expected_price = product.price * Decimal('0.80')
            self.assertEqual(product.get_price_with_discount(), expected_price)

    def test_get_price_in_product_category_and_product_promotion(self):
        category = Category.objects.create(user=self.test_user, name="Electronics")

        promotion = Promotion.objects.create(
            discount_percentage=20,
            start_date=timezone.now() - timezone.timedelta(days=7),
            end_date=timezone.now() + timezone.timedelta(days=7),
            user=self.test_user
        )
        promotion.categories.add(category)
        promotion.save()

        products = [
            Product.objects.create(user=self.test_user, barcode="P1", name="Product 1", price=Decimal('100.00'), category=category),
            Product.objects.create(user=self.test_user, barcode="P2", name="Product 2", price=Decimal('200.00'), category=category),
            Product.objects.create(user=self.test_user, barcode="P3", name="Product 3", price=Decimal('300.00'), category=category),
        ]

        promotion.products.add(products[0])
        promotion.save()

        for product in products:
            expected_price = product.price * Decimal('0.80')
            self.assertEqual(product.get_price_with_discount(), expected_price)
    
    def test_promotion_active_before_start_date(self):
        """
        Test case to verify that a promotion is not active before its start date.
        """
        future_promotion = Promotion.objects.create(
            user=self.test_user,
            name='Future Promotion',
            description='This promotion is in the future',
            discount_percentage=10.00,
            start_date=timezone.now() + timezone.timedelta(days=7),
            end_date=timezone.now() + timezone.timedelta(days=14),
            status=True
        )

        self.assertFalse(future_promotion.is_active())
    
    def test_promotion_active_on_start_date(self):
        """
        Test case to verify that a promotion is active on its start date.
        """
        active_promotion = Promotion.objects.create(
            user=self.test_user,
            name='Active Promotion',
            description='This promotion is active',
            discount_percentage=5.00,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=7),
            status=True
        )

        self.assertTrue(active_promotion.is_active())
    
    def test_promotion_active_between_start_and_end_dates(self):
        """
        Test case to verify that a promotion is active between its start and end dates.
        """
        active_promotion = Promotion.objects.create(
            user=self.test_user,
            name='Active Promotion',
            description='This promotion is active',
            discount_percentage=5.00,
            start_date=timezone.now() - timezone.timedelta(days=7),
            end_date=timezone.now() + timezone.timedelta(days=7),
            status=True
        )

        self.assertTrue(active_promotion.is_active())
    
    def test_promotion_active_on_end_date(self):
        """
        Test case to verify that a promotion is active on its end date.
        """
        active_promotion = Promotion.objects.create(
            user=self.test_user,
            name='Active Promotion',
            description='This promotion is active',
            discount_percentage=5.00,
            start_date=timezone.now() - timezone.timedelta(days=7),
            end_date=timezone.now(),
            status=True
        )

        self.assertFalse(active_promotion.is_active())
    
    def test_promotion_active_after_end_date(self):
        """
        Test case to verify that a promotion is not active after its end date.
        """
        expired_promotion = Promotion.objects.create(
            user=self.test_user,
            name='Expired Promotion',
            description='This promotion has expired',
            discount_percentage=15.00,
            start_date=timezone.now() - timezone.timedelta(days=14),
            end_date=timezone.now() - timezone.timedelta(days=7),
            status=True
        )

        self.assertFalse(expired_promotion.is_active())
    
    def test_promotion_not_active_after_end_date(self):
        
        """
        Test case to verify that a promotion is not active after its end date.
        """
        expired_promotion = Promotion.objects.create(
            user=self.test_user,
            name='Expired Promotion',
            description='This promotion has expired',
            discount_percentage=15.00,
            start_date=timezone.now() - timezone.timedelta(days=14),
            end_date=timezone.now() - timezone.timedelta(days=7),
            status=True
        )

        self.assertFalse(expired_promotion.is_active())