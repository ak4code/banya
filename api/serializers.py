from django.contrib.auth.models import User
from rest_framework import serializers
from store.models import Category, Product, Order, OrderItem


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name']


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True, source='get_absolute_url')
    counts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def get_counts(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True, source='get_absolute_url')
    small_img = serializers.CharField(read_only=True, source='get_small_img')
    medium_img = serializers.CharField(read_only=True, source='get_medium_img')
    full_img = serializers.CharField(read_only=True, source='get_full_img')
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True, required=False)
    shipping = serializers.CharField(source='get_shipping_type_display', read_only=True)
    customer_info = CustomerSerializer(source='customer', read_only=True)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items:
            OrderItem.objects.create(order=order, **item)
        return order
