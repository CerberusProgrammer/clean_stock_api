from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Product
from .models import Supplier
from .models import Category
from .models import Manufacturer
from .models import Order
from .models import Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'allow_blank': False, 'min_length': 8}, 'email': {'required': True, 'allow_blank': False,  'max_length': 255}, 'username': {'required': True, 'allow_blank': False, 'max_length': 150,}}
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Product
        fields = '__all__'
    
    def validate(self, data):
        user = self.context['request'].user
        barcode = data.get('barcode')
        if Product.objects.filter(user=user, barcode=barcode).exists():
            raise serializers.ValidationError({"barcode": "Product with this barcode already exists for this user."})
        return data

class SupplierSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Supplier
        fields = '__all__'
    
    def validate(self, data):
        user = self.context['request'].user
        name = data['name']
        if Supplier.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError({"name": "Supplier with this field already exists for this user."})
        return data

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Category
        fields = '__all__'
    
    def validate(self, data):
        user = self.context['request'].user
        name = data['name']
        if Category.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError({"name": "Category with this field already exists for this user."})
        return data

class ManufacturerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Manufacturer
        fields = '__all__'
    
    def validate(self, data):
        user = self.context['request'].user
        name = data['name']
        if Manufacturer.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError({"name": "Manufacturer with this field already exists for this user."})
        return data

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Order
        fields = '__all__'
    
    def validate(self, data):
        user = self.context['request'].user
        order_number = data['order_number']
        if Order.objects.filter(user=user, order_number=order_number).exists():
            raise serializers.ValidationError({"order_number": "Order with this number already exists for this user."})
        return data

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        transaction_id = data['transaction_id']
        if Transaction.objects.filter(user=user, transaction_id=transaction_id).exists():
            raise serializers.ValidationError({"transaction_id": "Transaction with this ID already exists for this user."})
        return data