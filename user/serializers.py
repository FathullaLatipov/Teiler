from collections import defaultdict

from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password

from user.models import CustomUser


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
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user_data'] = UserDataSerializer(self.user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, required=False,
                                     write_only=True)

    password2 = serializers.CharField(max_length=255, required=False,
                                     write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        extra_kwargs = dict(
            password=dict(required=True)
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
        password = attrs.get('password', '')
        user = auth.authenticate(password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again pls')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'username': user.username,
            'password': user.password,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
