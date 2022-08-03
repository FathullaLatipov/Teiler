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

    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     try:
    #         account = CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
    #     except CustomUser.DoesNotExist:
    #         return email
    #     raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def save(self, commit=True):
        account = super(CustomUserChangeForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        if commit:
            account.save()
        return account
