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

from stock.models import Order
from stock.models import Product
from stock.models import Category
from stock.models import Supplier
from stock.models import Promotion
from stock.models import Transaction
from stock.models import Manufacturer

from stock.filters import OrderFilter
from stock.filters import ProductFilter
from stock.filters import CategoryFilter
from stock.filters import SupplierFilter
from stock.filters import PromotionFilter
from stock.filters import TransactionFilter
from stock.filters import ManufacturerFilter

from stock.serializers import UserSerializer
from stock.serializers import OrderSerializer
from stock.serializers import ProductSerializer
from stock.serializers import SupplierSerializer
from stock.serializers import CategorySerializer
from stock.serializers import PromotionSerializer
from stock.serializers import TransactionSerializer
from stock.serializers import ManufacturerSerializer

from django.db.models import F 
from django.db.models import Sum 
from django.utils import timezone
from django.db.models.functions import TruncDay


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
    
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.cancel()
        return Response({"status": "Order cancelled."})

    @action(detail=False, methods=['get'], url_path='fast-report')
    def fast_report(self, request):
        one_week_ago = timezone.now() - timezone.timedelta(days=7)
        orders = Order.objects.filter(user=request.user, created_at__gte=one_week_ago)

        total_earned = orders.annotate(total_order=Sum(F('transactions__price') * F('transactions__quantity'))).aggregate(Sum('total_order'))['total_order__sum'] or 0
        total_transactions = orders.aggregate(total=Sum('transactions__quantity'))['total'] or 0
        number_of_orders = orders.count()
        average_earnings_per_order = total_earned / number_of_orders if number_of_orders > 0 else 0

        product_sales = Transaction.objects.filter(order__in=orders).values('product').annotate(total_sold=Sum('quantity')).order_by('-total_sold').first()
        most_sold_product = Product.objects.get(id=product_sales['product']) if product_sales else None

        transactions_by_day = {}
        daily_transactions = Transaction.objects.filter(order__in=orders).annotate(day=TruncDay('created_at')).order_by('day')
        for transaction in daily_transactions:
            day_name = transaction.created_at.strftime('%A').lower()
            if day_name not in transactions_by_day:
                transactions_by_day[day_name] = []
            transactions_by_day[day_name].append(TransactionSerializer(transaction).data)

        weekly_sales = []
        for order in orders:
            transactions = order.transactions.all().values('product__name', 'quantity', 'price')
            weekly_sales.append({
                'order_id': order.id,
                'created_at': order.created_at,
                'transactions': list(transactions),
            })

        different_days = 7
        daily_average = total_transactions / different_days if different_days > 0 else 0

        report = {
            'total_earned': total_earned,
            'total_transactions': total_transactions,
            'number_of_orders': number_of_orders,
            'average_earnings_per_order': average_earnings_per_order,
            'most_sold_product': ProductSerializer(most_sold_product).data if most_sold_product else None,
            'daily_transactions_average': daily_average,
            'sales_last_week': weekly_sales,
            'transactions_by_day': transactions_by_day,
        }

        return Response(report)

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