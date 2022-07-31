from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'last_name', 'email', 'phone')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'last_name', 'email', 'phone')
