from django.contrib import admin

from .models import Order, Product, Category, Manufacturer, Promotion, Supplier, Transaction

admin.site.site_header = 'Stock Management System'
admin.site.site_title = 'Stock Management System'
admin.site.index_title = 'Stock Management System'

admin.site.register(Promotion)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Supplier)
admin.site.register(Order)
admin.site.register(Transaction)