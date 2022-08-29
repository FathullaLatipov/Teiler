from django import forms

from .models import OrderModel


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        label = 'Test'
        fields = ['online', 'upon_receipt', 'status', 'user',]
        widgets = {
            'online': forms.RadioSelect(),
            'upon_receipt': forms.RadioSelect(),
            'status': forms.RadioSelect(),
            'user': forms.HiddenInput()
        }
