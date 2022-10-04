from django.db.models import Min, Max, Count, Avg
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import Serializer
from rest_framework.relations import PrimaryKeyRelatedField

from carousel.models import CarouselModel
from help.models import HelpModel
from .models import ProductModel, ReviewModel, CategoryModel, ProductImageModel, ColorModel, ProductCustomNameModel, \
    ProductCharacteristicModel


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = ['rating']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = ['color_title', 'code']


class ProductSerializer(serializers.ModelSerializer):
    rating = ProductRatingSerializer(many=True, default=None)
    current_color = ProductColorSerializer(many=True)

    # rating = serializers.SerializerMethodField()

    # max_price = serializers.SerializerMethodField()
    # min_price = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    # subcategory = serializers.SlugRelatedField(slug_field='subcategory', read_only=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'title', 'sku', 'image', 'current_chars', 'current_color', 'discount', 'price',
                  'get_price', 'is_published', 'is_fav', 'rating', 'status',
                  ]

    def to_representation(self, instance):

        data = super().to_representation(instance)
        if data['rating'] == []:
            data['rating'] = 0
        else:
            data['rate_count'] = instance.rating.count()
        return data


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['title', 'discount']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['discount'] == "0":
            data = {
                "discount": "null"
            }
        else:
            pass

        return data

    # def get_min_price(self, obj):
    #     min_price = ProductModel.objects.all().aggregate(min_price=Min('real_price'))
    #     return min_price['min_price']
    #
    # def get_max_price(self, obj):
    #     max_price = ReviewModel.objects.all().aggregate(max_price=Avg('rating'))
    #     return max_price['max_price']


class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = ['image']


class ProductCharacteristicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharacteristicModel
        fields = ['chars_title', 'chars_number']


class ProductDetailSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    # subcategory = serializers.SlugRelatedField(slug_field='subcategory', read_only=True)
    brand = serializers.SlugRelatedField(slug_field='brand', read_only=True)
    current_color = ProductColorSerializer(many=True)
    rating = ProductRatingSerializer(many=True)
    images = ProductImageModelSerializer(many=True)
    characteristics = ProductCharacteristicModelSerializer(many=True)
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ['sku', 'title', 'discount', 'price', 'get_price', 'rating', 'images', 'img_url', 'current_color',
                  'is_published', 'description', 'options', 'characteristics', 'brand',
                  ]

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['rating'] == []:
            data['rating'] = 0
        else:
            data['rate_count'] = instance.rating.count()
        if data['options'] == []:
            data['options'] = 0
        else:
            data['options'] = ["Вот сюда ты берешь все значения current chars и current colors продуктов у которого одинаковый title(iphone13)"]
        return data


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselModel
        fields = ['title', 'descriptions', 'background_image']


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpModel
        fields = ['title', 'category', 'subcategory', 'descriptions']


# class SubCategorySerializerField(serializers.RelatedField):
#     def to_representation(self, value):
#         queryset = CategoryModel.objects.all()
#         return queryset

class RecursiveField(Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(many=True)

    class Meta:
        model = CategoryModel
        fields = ['id', 'title', 'subcategories', 'image']


class ReviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['id', 'title']


class ReviewModelSerializer(serializers.ModelSerializer):
    product = ReviewProductSerializer()

    class Meta:
        model = ReviewModel
        fields = ['name', 'email', 'image', 'rating', 'comments', 'product', 'created_at']
