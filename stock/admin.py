from django.contrib import admin

from .models import Order, Product, Category, Manufacturer, Supplier, Transaction

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Supplier)
admin.site.register(Order)
admin.site.register(Transaction)