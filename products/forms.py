from django import forms
from django.forms import BaseForm, inlineformset_factory

from products import models
from products.models import ColorModel, ReviewModel, RegisterForm, ProductModel


class ColorModelForm(forms.ModelForm):
    class Meta:
        model = ColorModel
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(
                attrs={'type': 'color'}
            )
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ("name", "email", "comments", "image", "rating")


class SingleProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = '__all__'
