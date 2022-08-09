from django import forms

from .models import OrderModel


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['first_name', 'last_name', 'email']
