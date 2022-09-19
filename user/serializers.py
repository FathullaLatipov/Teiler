from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

from user.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

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