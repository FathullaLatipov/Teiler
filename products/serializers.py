from django.db.models import Min, Max
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from rest_framework import serializers

from carousel.models import CarouselModel
from help.models import HelpModel
from .models import ProductModel, ReviewModel, CategoryModel, SubCategoryModel


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = ['rating']


class ProductSerializer(serializers.ModelSerializer):
    rating = ProductRatingSerializer(many=True)
    max_price = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    subcategory = serializers.SlugRelatedField(slug_field='subcategory', read_only=True)

    class Meta:
        model = ProductModel
        fields = ['title', 'id', 'sku', 'category', 'subcategory', 'image', 'price',
                  'discount', 'get_price', 'is_published', 'rating',
                  'min_price', 'max_price',
                  ]

    def get_min_price(self, obj):
        min_price = ProductModel.objects.all().aggregate(min_price=Min('real_price'))
        return min_price['min_price']

    def get_max_price(self, obj):
        max_price = ProductModel.objects.all().aggregate(max_price=Max('real_price'))
        return max_price['max_price']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    subcategory = serializers.SlugRelatedField(slug_field='subcategory', read_only=True)
    brand = serializers.SlugRelatedField(slug_field='brand', read_only=True)
    colors = serializers.SlugRelatedField(slug_field='code', read_only=True, many=True)
    rating = ProductRatingSerializer(many=True)

    class Meta:
        model = ProductModel
        fields = '__all__'


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselModel
        fields = ['title', 'descriptions', 'background_image']


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpModel
        fields = ['title', 'category', 'subcategory', 'descriptions']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'title', 'image']


class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = SubCategoryModel
        fields = '__all__'
