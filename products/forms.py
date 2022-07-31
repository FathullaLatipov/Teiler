from django import forms
from django.forms import BaseForm
from products.models import ColorModel, RatingStar, ReviewModel, RegisterForm


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
