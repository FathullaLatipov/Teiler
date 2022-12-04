import django_filters

from orders.models import OrderItem
from products.models import ProductModel


class ModelFilter(django_filters.FilterSet):
    product = django_filters.ModelChoiceFilter(field_name="product__status",
                                               queryset=ProductModel.objects.all())

    class Meta:
        model = OrderItem
        fields = ('product',)
