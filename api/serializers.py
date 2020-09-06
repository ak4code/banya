from rest_framework import serializers
from store.models import Category, Product, Order, OrderItem


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

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items:
            OrderItem.objects.create(order=order, **item)
        return order
