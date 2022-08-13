from django import forms

from .models import OrderModel


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        label = 'Test'
        fields = ['first_name', 'last_name', 'email', 'phone', 'online', 'upon_receipt', 'user_order', 'user']
        widgets = {
            'online': forms.RadioSelect(),
            'upon_receipt': forms.RadioSelect(),
            'user_order': forms.RadioSelect(),
            'user': forms.HiddenInput()
        }
