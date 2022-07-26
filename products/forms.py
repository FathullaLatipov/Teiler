from django import forms
from django.forms import BaseForm

from products.models import ColorModel, RatingStar, Rating, ReviewModel


class ColorModelForm(forms.ModelForm):
    class Meta:
        model = ColorModel
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(
                attrs={'type': 'color'}
            )
        }


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ("name", "email", "comments", "image", "rating")
