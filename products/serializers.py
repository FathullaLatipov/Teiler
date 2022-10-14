from django.db.models import Min, Max, Count, Avg
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import Serializer
from rest_framework.relations import PrimaryKeyRelatedField

from carousel.models import CarouselModel
from help.models import HelpModel
from .models import ProductModel, ReviewModel, CategoryModel, ProductImageModel, ColorModel, \
    ProductCharacteristicModel, ProductAttributes, ProductOptionsModel, ReviewImageModel


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = ['rating']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = ['color_title', 'code', 'color_type']


class ProductSerializer(serializers.ModelSerializer):
    rating = ProductRatingSerializer(many=True, default=None)

    # сolors = ProductColorSerializer(many=True)

    # rating = serializers.SerializerMethodField()

    # max_price = serializers.SerializerMethodField()
    # min_price = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    # subcategory = serializers.SlugRelatedField(slug_field='subcategory', read_only=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'title', 'image', 'discount', 'price',
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


class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionsModel
        exclude = ['product', 'id', 'created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    # subcategory = serializers.SlugRelatedField(slug_field='subcategory', read_only=True)
    brand = serializers.SlugRelatedField(slug_field='brand', read_only=True)
    сolors = ProductColorSerializer(many=True)
    rating = ProductRatingSerializer(many=True)
    images = ProductImageModelSerializer(many=True)
    characteristics = ProductCharacteristicModelSerializer(many=True)
    img_url = serializers.SerializerMethodField()
    products_options = ProductAttributesSerializer(many=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'sku', 'title', 'images', 'discount', 'price', 'get_price', 'rating', 'img_url', 'is_published',
                  'condition', 'products_options', 'сolors', 'characteristics', 'description', 'brand',
                  ]

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['rating'] == []:
            data['rating'] = 0
        else:
            data['rate_count'] = instance.rating.count()
        if data['products_options'] == []:
            data['products_options'] = 0
        else:
            data['products_options']
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


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImageModel
        fields = ['image', ]


class ReviewModelSerializer(serializers.ModelSerializer):
    product = ReviewProductSerializer()
    images = ReviewImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(allow_null=True, required=False,
        child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=False, required=False),
    )

    class Meta:
        model = ReviewModel
        fields = ['name', 'email', 'images', 'uploaded_images', 'rating', 'comments', 'product', 'created_at']

    # def create(self, validated_data):
    #     uploaded_data = validated_data.pop('uploaded_images')
    #     new_product = ReviewModel.objects.create(**validated_data)
    #     for uploaded_item in uploaded_data:
    #         new_product_image = ReviewImageModel.objects.create(product=new_product, images=uploaded_item)
    #     return new_product
    # return ReviewModel.objects.create(**validated_data)


class ReviewCreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['pk', ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    product = ReviewCreateProductSerializer()
    images = ReviewImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = ReviewModel
        fields = ['name', 'email', 'images', 'uploaded_images', 'rating', 'comments', 'product.pk', 'created_at']

    def create(self, validated_data):
        uploaded_data = validated_data.pop('uploaded_images')
        new_product = ReviewModel.objects.create(**validated_data)
        for uploaded_item in uploaded_data:
            new_product_image = ReviewImageModel.objects.create(product=new_product, images=uploaded_item)
        return new_product
