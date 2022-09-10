from rest_framework import serializers

from .models import ProductModel


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['title', 'sku', 'image', 'price', 'discount', 'get_price', 'is_published']
