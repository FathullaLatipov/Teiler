from django import template
from products.models import ProductModel

register = template.Library()


@register.simple_tag
def get_price(request, x):
    price = request.GET.get('price')
    print(price)
    if price:
        return price.split(';')[x]
    return 'null'

