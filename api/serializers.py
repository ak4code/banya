from rest_framework import serializers
from store.models import Category, Product


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
