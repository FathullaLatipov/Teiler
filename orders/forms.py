from django import forms

from .models import OrderModel


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        label = 'Test'
        fields = ['first_name', 'last_name', 'email', 'online', 'upon_receipt']
        widgets = {
            'online': forms.RadioSelect(),
            'upon_receipt': forms.RadioSelect(),
        }
