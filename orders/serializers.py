from rest_framework import serializers

from orders.models import OrderModel, OrderItem
from products.models import ProductModel, BrandModel
from products.serializers import ProductColorSerializer, CategorySerializer
from user.models import CustomUser


class OrderProductsSerializer(serializers.ModelSerializer):
    сolors = ProductColorSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = ProductModel
        exclude = ['brand']


class OrderCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserSer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'last_name', 'first_name']


class UserSerializer(serializers.ModelSerializer):
    user = CustomUserSer

    class Meta:
        model = OrderModel
        fields = ['online', 'upon_receipt', 'status', 'user', 'phone', 'email', 'address', 'flat_office', 'entrance',
                  'intercom', 'floor', 'coupon', 'discount', 'created_at', 'updated_at', 'paid', 'order']

    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('accountprofile')
    #     profile = instance.accountprofile
    #
    #     # * User Info
    #     instance.first_name = validated_data.get(
    #         'first_name', instance.first_name)
    #     instance.last_name = validated_data.get(
    #         'last_name', instance.last_name)
    #     instance.email = validated_data.get(
    #         'email', instance.email)
    #     instance.save()
    #
    #     # * AccountProfile Info
    #     profile.gender = profile_data.get(
    #         'gender', profile.gender)
    #     profile.phone = profile_data.get(
    #         'phone', profile.phone)
    #     profile.location = profile_data.get(
    #         'location', profile.location)
    #     profile.birth_date = profile_data.get(
    #         'birth_date', profile.birth_date)
    #     profile.biodata = profile_data.get(
    #         'biodata', profile.biodata)
    #     profile.save()
    #
    #     return instance


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductsSerializer()
    order = UserSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'
