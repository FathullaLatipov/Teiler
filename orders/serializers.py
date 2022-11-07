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


class UserSerializer(serializers.ModelSerializer):
    user = OrderCustomUserSerializer()

    class Meta:
        model = OrderModel
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductsSerializer()
    order = UserSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'
