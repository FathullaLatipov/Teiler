from django import template
from products.models import ProductModel

register = template.Library()


@register.filter()
def in_wishlist(wishlist, request):
    return wishlist.pk in request.session.get('wishlist', [])


@register.simple_tag
def get_wishlist_count(request):
    wishlist = request.session.get('wishlist')
    if wishlist:
        return len(wishlist)
    return 0


@register.simple_tag
def get_price(request, x):
    price = request.GET.get('price')
    print(price)
    if price:
        return price.split(';')[x]
    return 'null'
