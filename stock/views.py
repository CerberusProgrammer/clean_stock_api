from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from stock.models import Product
from stock.models import Category
from stock.models import Supplier
from stock.models import Manufacturer
from stock.models import Order
from stock.models import Transaction

from stock.filters import ProductFilter
from stock.filters import CategoryFilter
from stock.filters import SupplierFilter
from stock.filters import ManufacturerFilter
from stock.filters import OrderFilter
from stock.filters import TransactionFilter

from stock.serializers import CategorySerializer
from stock.serializers import ManufacturerSerializer
from stock.serializers import ProductSerializer
from stock.serializers import SupplierSerializer
from stock.serializers import OrderSerializer
from stock.serializers import TransactionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SupplierFilter

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ManufacturerFilter

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter