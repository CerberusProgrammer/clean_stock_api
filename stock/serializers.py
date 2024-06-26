from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Product, Promotion
from .models import Supplier
from .models import Category
from .models import Manufacturer
from .models import Order
from .models import Transaction

class PromotionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Promotion
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        if Promotion.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError({"name": "Promotion with this name already exists for this user."})
        
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"end_date": "End date must be greater than start date."})
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'allow_blank': False, 'min_length': 8}, 'email': {'required': True, 'allow_blank': False,  'max_length': 255}, 'username': {'required': True, 'allow_blank': False, 'max_length': 150,}}
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    price = serializers.FloatField()
    weight = serializers.FloatField()

    class Meta:
        model = Product
        fields = '__all__'
    
    def validate(self, data):
        user = self.context['request'].user
        barcode = data.get('barcode')
        
        if Product.objects.filter(user=user, barcode=barcode).exists():
            raise serializers.ValidationError({"barcode": "Product with this barcode already exists for this user."})
        
        quantity = data.get('quantity')
        quantity_min = data.get('quantity_min')
        quantity_max = data.get('quantity_max')

        if quantity_min is not None and quantity < quantity_min:
            raise serializers.ValidationError({'quantity': 'Quantity must be greater than or equal to quantity_min.'})
        if quantity_max is not None and quantity > quantity_max:
            raise serializers.ValidationError({'quantity': 'Quantity must be less than or equal to quantity_max.'})

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
        transactions = data.get('transactions')
        if not transactions:
            raise serializers.ValidationError({"transactions": "At least one transaction is required."})
        
        return data

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, data):
        product = data.get('product')
        
        if not product:
            raise serializers.ValidationError({"product": "At least one transaction is required."})
        
        return data