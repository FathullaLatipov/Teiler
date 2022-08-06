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


class UserNameChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)


class LastNameChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('last_name',)


class DateBrithChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('date_birth',)


class MaleChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('male',)


class PhoneChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone',)


class EmailChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class PasswordChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('password',)

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
        account.phone = self.cleaned_data['phone']
        account.email = self.cleaned_data['email'].lower()
        if commit:
            account.save()
        print(self.cleaned_data)
        return account
