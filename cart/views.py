from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404

from products.models import ProductModel
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect(request.GET.get('next', '/'))

@require_POST
def single_cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    cart.remove(product)
    return redirect(request.GET.get('next', '/'))


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    coupon_apply_form = CouponApplyForm()

    context = {'cart': cart, 'coupon_apply_form': coupon_apply_form}
    return render(request, 'cart/detail.html', context)


@require_POST
def add_to_card_from_product_page(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        print(data)
    return redirect(request.GET.get('next', '/'))



