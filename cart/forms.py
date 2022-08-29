from django import forms

from user.models import CustomUser

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    # stat1 = forms.CharField(max_length=50, required=False)
    # stat2 = forms.CharField(max_length=50, required=False)
    # color = forms.CharField(max_length=50, required=False)
