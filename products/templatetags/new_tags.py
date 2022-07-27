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


@register.filter()
def in_cart(cart, request):
    return cart.pk in request.session.get('cart', [])


@register.simple_tag
def get_cart_count(request):
    cart = request.session.get('cart')
    if cart:
        return len(cart)
    return 0


@register.simple_tag
def get_price(request, x):
    price = request.GET.get('price')
    print(price)
    if price:
        return price.split(';')[x]
    return 'null'
