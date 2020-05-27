from rest_framework import serializers
from store.models import Category


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    counts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_counts(self, obj):
        return obj.products.count()
