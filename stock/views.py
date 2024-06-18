from django.shortcuts import render
from rest_framework import viewsets

from stock.models import Product
from stock.models import Category
from stock.models import Supplier
from stock.models import Manufacturer
from stock.serializers import CategorySerializer
from stock.serializers import ManufacturerSerializer
from stock.serializers import ProductSerializer
from stock.serializers import SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer