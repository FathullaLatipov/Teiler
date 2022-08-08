from django import forms
from django.forms import BaseForm, inlineformset_factory

from products import models, widgets
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


BasketLineFormSet = inlineformset_factory(
    models.BasketModel,
    models.BasketLine,
    fields=("quantity",),
    extra=0,
    widgets={"quantity": widgets.PlusMinusNumberInput()},
)


class AddressSelectionForm(forms.Form):
    billing_address = forms.ModelChoiceField(
        queryset=None
    )
    shipping_address = forms.ModelChoiceField(
        queryset=None
    )

    def __int__(self, instance, *args, **kwargs):
        super(). __init__(*args, **kwargs)
        queryset = models.AddressModel.objects.filter(user=self.user)
        self.fields['billing_address'].queryset = queryset
        self.fields['shipping_address'].queryset = queryset
