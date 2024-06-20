from django.db import models
from django.core.exceptions import ValidationError


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'barcode'], name='unique_barcode_per_user')
        ]
    
    def clean(self):
        if self.quantity_min is not None and self.quantity < self.quantity_min:
            raise ValidationError('Quantity must be greater than or equal to quantity_min.')
        if self.quantity_max is not None and self.quantity > self.quantity_max:
            raise ValidationError('Quantity must be less than or equal to quantity_max.')
    
    def __str__(self):
        return self.name

class Category(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, db_index=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)
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