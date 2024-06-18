
from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from stock.views import ProductViewSet
from stock.views import CategoryViewSet
from stock.views import SupplierViewSet
from stock.views import ManufacturerViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('suppliers', SupplierViewSet)
router.register('manufacturers', ManufacturerViewSet)

urlpatterns = [
    path('', include(router.urls))
]