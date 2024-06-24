
from django.urls import include
from django.urls import path

from stock.views import LoginView
from stock.views import UserViewSet
from stock.views import OrderViewSet
from stock.views import ProductViewSet
from stock.views import CategoryViewSet
from stock.views import SupplierViewSet
from stock.views import PromotionViewSet
from stock.views import TransactionViewSet
from stock.views import ManufacturerViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('orders', OrderViewSet)
router.register('products', ProductViewSet)
router.register('suppliers', SupplierViewSet)
router.register('categories', CategoryViewSet)
router.register('promotions', PromotionViewSet)
router.register('transactions', TransactionViewSet)
router.register('manufacturers', ManufacturerViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls))
]