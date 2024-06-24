from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

class Promotion(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[
            MinValueValidator(0.0, message="The discount percentage must be at least 0.0"),
            MaxValueValidator(100.00, message="The discount percentage cannot exceed 100.00")
        ]
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    products = models.ManyToManyField('Product', related_name='promotions', blank=True)
    categories = models.ManyToManyField('Category', related_name='promotions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    
    def is_active(self):
        return self.start_date <= timezone.now() <= self.end_date

class Product(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=100, db_index=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dimension = models.CharField(max_length=100, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, blank=True, null=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    status = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    quantity_min = models.IntegerField(blank=True, null=True)
    quantity_max = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'barcode'], name='unique_barcode_per_user')
        ]
    
    def get_price_with_discount(self):
        if not hasattr(self, '_price_with_discount'):
            self._price_with_discount = self.price
            active_product_promotions = self.promotions.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
            active_category_promotions = Promotion.objects.filter(categories=self.category, start_date__lte=timezone.now(), end_date__gte=timezone.now())
            
            active_promotions = active_product_promotions | active_category_promotions
            
            for promotion in active_promotions.distinct():
                self._price_with_discount *= (1 - (promotion.discount_percentage / 100))
                self._price_with_discount = max(self._price_with_discount, 0)
        return self._price_with_discount
    
    def __str__(self):
        return self.name

class Category(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, db_index=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_category_per_user')
        ]
    
    def __str__(self):
        return self.name

class Manufacturer(models.Model):    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_manufacturer_per_user')
        ]
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    status = models.BooleanField(default=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_supplier_per_user')
        ]
    
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    transactions = models.ManyToManyField('Transaction')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'created_at'], name='unique_order_per_user')
        ]
    
    def __str__(self):
        return f'{self.created_at} - {self.status} - {len(self.transactions.all())} transactions'

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            for transaction in self.transactions.all():
                transaction.product.quantity -= transaction.quantity
                transaction.product.save()
        else:
            super().save(*args, **kwargs)
    
    def cancel(self):
        if not self.status:
            raise ValueError("Order has already been cancelled")

        self.status = False
        for transaction in self.transactions.all():
            transaction.product.quantity += transaction.quantity
            transaction.product.save()
        self.save()

class Transaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product', 'created_at'], name='unique_transaction_per_user')
        ]
    
    def __str__(self):
        return self.product.name