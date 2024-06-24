from django_filters import rest_framework as filters

from stock.models import Product, Promotion
from stock.models import Category
from stock.models import Supplier
from stock.models import Manufacturer
from stock.models import Order
from stock.models import Transaction

class PromotionFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    start_date = filters.DateFilter(lookup_expr='exact')
    end_date = filters.DateFilter(lookup_expr='exact')
    created_at = filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = Promotion
        fields = ['name', 'description', 'start_date', 'end_date', 'created_at']

class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    barcode = filters.CharFilter(lookup_expr='icontains')
    weight = filters.NumberFilter(lookup_expr='exact')
    dimension = filters.CharFilter(lookup_expr='icontains')
    expiration_date = filters.DateFilter(lookup_expr='exact')
    location = filters.CharFilter(lookup_expr='icontains')
    manufacturer = filters.CharFilter(lookup_expr='icontains')
    supplier = filters.CharFilter(lookup_expr='icontains')
    status = filters.BooleanFilter(lookup_expr='exact')
    price = filters.NumberFilter(lookup_expr='exact')
    quantity = filters.NumberFilter(lookup_expr='exact')
    category = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['name', 'description', 'barcode', 'weight', 'category', 'dimension', 'expiration_date', 'location', 'manufacturer', 'supplier','status', 'price', 'quantity', 'created_at']

class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = Category
        fields = ['name', 'description', 'created_at']

class SupplierFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    contact_phone = filters.CharFilter(lookup_expr='icontains')
    contact_email = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = Supplier
        fields = ['name', 'description', 'contact_phone', 'contact_email', 'address', 'created_at']

class ManufacturerFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    contact_phone = filters.CharFilter(lookup_expr='icontains')
    contact_email = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFilter(lookup_expr='exact')
    website = filters.CharFilter(lookup_expr='icontains')
    country = filters.CharFilter(lookup_expr='icontains')
    city = filters.CharFilter(lookup_expr='icontains')
    status = filters.BooleanFilter(lookup_expr='exact')

    class Meta:
        model = Manufacturer
        fields = ['name', 'description', 'contact_phone', 'contact_email', 'address', 'created_at', 'website', 'country', 'city', 'status',]

class OrderFilter(filters.FilterSet):
    created_at = filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = Order
        fields = ['created_at']

class TransactionFilter(filters.FilterSet):
    product = filters.CharFilter(lookup_expr='icontains')
    quantity = filters.NumberFilter(lookup_expr='exact')
    price = filters.NumberFilter(lookup_expr='exact')
    created_at = filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = Transaction
        fields = ['product', 'quantity', 'price', 'created_at']