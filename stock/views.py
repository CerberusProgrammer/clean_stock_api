from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from stock.models import Product, Promotion
from stock.models import Category
from stock.models import Supplier
from stock.models import Manufacturer
from stock.models import Order
from stock.models import Transaction

from stock.filters import ProductFilter, PromotionFilter
from stock.filters import CategoryFilter
from stock.filters import SupplierFilter
from stock.filters import ManufacturerFilter
from stock.filters import OrderFilter
from stock.filters import TransactionFilter

from stock.serializers import CategorySerializer, PromotionSerializer, UserSerializer
from stock.serializers import ManufacturerSerializer
from stock.serializers import ProductSerializer
from stock.serializers import SupplierSerializer
from stock.serializers import OrderSerializer
from stock.serializers import TransactionSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]
        return super(self.__class__, self).get_permissions()

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PromotionFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Promotion.objects.filter(user=self.request.user).order_by('-id')
        return Promotion.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Product.objects.filter(user=self.request.user).order_by('-id')
        return Product.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Category.objects.filter(user=self.request.user).order_by('id')
        return Category.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SupplierFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Supplier.objects.filter(user=self.request.user).order_by('id')
        return Supplier.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ManufacturerFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Manufacturer.objects.filter(user=self.request.user).order_by('id')
        return Manufacturer.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user).order_by('-created_at')
        return Order.objects.none()
    
    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)

        for transaction in order.transactions.all():
            transaction.product.quantity -= transaction.quantity
            transaction.product.save()
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.cancel()
        return Response({"status": "Order cancelled."})

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Transaction.objects.filter(user=self.request.user).order_by('-created_at')
        return Transaction.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)