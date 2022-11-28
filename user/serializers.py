from collections import defaultdict

from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

from orders.models import OrderItem, OrderModel
from products.serializers import ProductSerializer
from user.models import CustomUser, AdressInfoModel


class CheckTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class UserDataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False,
                                     validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, attrs):
        if password := attrs.get('password'):
            attrs['password'] = make_password(password)
        return attrs


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    extra_kwargs = dict(
        password=dict(required=True),
        username=dict(required=True),
    )

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = str(self.user)
        data['user_id'] = str(self.user.id)
        data['status'] = str('Success')

        password = attrs.get('password', '')
        username = attrs.get('username', '')
        user_pass = auth.authenticate(password=password)
        user = CustomUser.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('нужен username')
        if not user.check_password(password):
            raise AuthenticationFailed('нужен password')

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data

    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #
    #     refresh = self.get_token(self.user)
    #
    #     data['refresh'] = str(refresh)
    #     data['access'] = str(refresh.access_token)
    #     data['user_data'] = UserDataSerializer(self.user).data
    #     data['user'] = str(self.user)
    #     data['user_id'] = str(self.user.id)
    #     data['status'] = str('Success')
    #
    #     if api_settings.UPDATE_LAST_LOGIN:
    #         update_last_login(None, self.user)
    #
    #     return data


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, required=False,
                                      write_only=True)

    password2 = serializers.CharField(max_length=255, required=False,
                                      write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'date_birth',
                  'sex']
        extra_kwargs = dict(
            password=dict(required=True),
            date_birth={"read_only": True},
            sex={"read_only": True},
        )

    def validate(self, attrs):
        errors = defaultdict(list)
        users = CustomUser.objects.filter(username=attrs['username'])
        emails = CustomUser.objects.filter(email=attrs['email'])
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if self.instance:
            users = users.exclude(pk=self.instance.id)
        if users.exists():
            errors['username'].append('Username has already token')
        if emails.exists():
            errors['email'].append('Email has already')
        if errors:
            raise serializers.ValidationError(errors)
        if password1 != password2:
            raise serializers.ValidationError(
                {'status': "Password do not match"}
            )
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1', None)
        password2 = validated_data.pop('password2', None)
        user = super().create(validated_data)
        if password1:
            user.set_password(password1)
            user.set_password(password2)
            user.save()
        return user

    def update(self, instance, validated_data):
        password1 = validated_data.pop('password1', None)
        password2 = validated_data.pop('password2', None)
        user = super().update(instance, validated_data)
        if password1:
            user.set_password(password1)
            user.set_password(password2)
            user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=255, min_length=3)

    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'tokens']

    def validate(self, attrs):
        data = super().validate(attrs)
        password = attrs.get('password', '')
        user = auth.authenticate(password=password)

        if not user:
            raise AuthenticationFailed('Пароль обязательное поле*')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'username': user.username,
            'password': user.password,
            'tokens': user.tokens
        }

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['id', 'online', 'upon_receipt', 'status', 'user', 'paid']


class UserOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity']


class UserInfoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'date_birth', 'sex', 'points', 'phone', 'email', 'password')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'date_birth', 'sex', 'phone', 'email', 'password')
        extra_kwargs = {
            'username': {'required': False},
            'password': {'required': False},
        }

    def update(self, instance, validated_data):
        print(instance, validated_data)
        # user = self.context['request'].user
        #
        # if user.pk != instance.pk:
        #     raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        # if 'username' in validated_data:
        # if 'first_name' in validated_data:
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        # if 'date_birth' in validated_data:
        instance.date_birth = validated_data['date_birth']
        # if 'sex' in validated_data:
        instance.sex = validated_data['sex']
        # if 'email' in validated_data:
        # if 'email' not in validated_data:
        instance.email = validated_data['email']
        # if 'phone' in validated_data:
        instance.phone = validated_data['phone']
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        else:
            return instance

        instance.save()

        return instance


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', ]


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdressInfoModel
        fields = ['pk', 'address', 'lat', 'lng', 'is_house', 'comment', 'user']
        extra_kwargs = dict(
            user={"read_only": True},
        )


class DeleteAddresUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdressInfoModel
        fields = ['pk', 'address', 'lat', 'lng', 'is_house', 'comment', 'user']
        extra_kwargs = dict(
            user={"read_only": True},
        )


class AddresUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdressInfoModel
        fields = ['pk', 'address', 'lat', 'lng', 'is_house', 'comment', ]
        extra_kwargs = dict(
            user={"read_only": True},
        )

    @swagger_auto_schema(
        operation_summary="Update address(PUT)",
        operation_description="Method for create ratings(POST)",
    )
    def update(self, instance, validated_data):
        print(instance, validated_data)
        # user = self.context['request'].user
        #
        # if user.pk != instance.pk:
        #     raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        # if 'username' in validated_data:
        # if 'first_name' in validated_data:
        instance.address = validated_data['address']
        instance.lat = validated_data['lat']
        # if 'date_birth' in validated_data:
        instance.lng = validated_data['lng']
        # if 'sex' in validated_data:
        instance.is_house = validated_data['is_house']
        # if 'email' in validated_data:
        # if 'email' not in validated_data:
        instance.comment = validated_data['comment']
        # if 'phone' in validated_data:
        # instance.user = validated_data['user']
        # if 'password' in validated_data:
        #     instance.set_password(validated_data['password'])
        # else:
        #     return instance

        instance.save()

        return instance
