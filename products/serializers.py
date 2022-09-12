from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from rest_framework import serializers

from carousel.models import CarouselModel
from .models import ProductModel, ReviewModel


class ProductRatingSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = ReviewModel
        fields = ['rating', 'product']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ['title', 'sku', 'category', 'subcategory', 'image', 'price', 'discount', 'get_price', 'is_published']


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselModel
        fields = ['title', 'descriptions', 'background_image']

