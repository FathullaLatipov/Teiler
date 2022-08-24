from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from coupons.forms import CouponApplyForm
from products.models import ProductModel
from user.models import CustomUser
from .models import OrderItem, OrderModel
from .forms import OrderCreateForm
from cart.cart import Cart


@login_required(login_url="login")
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            coupon_apply_form = CouponApplyForm()
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order, 'coupon_apply_form': coupon_apply_form})

    else:
        form = OrderCreateForm()
        coupon_apply_form = CouponApplyForm()

    return render(request, 'orders/order/create.html',
                  {'form': form, 'cart': cart, 'coupon_apply_form': coupon_apply_form})


@login_required(login_url="signup")
def user_order_view(request, user_pk):
    user = CustomUser.objects.get(pk=user_pk)
    user_orders = user.user_order.all()
    order_items = OrderItem.objects.select_related('product').filter(order__user_id=request.user)

    return render(request, 'lk.html', {'user_orders': user_orders,
                                       'order_items': order_items
                                       })



# def create_order(request):
#     user = user
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             form.cleaned_data['first_name'] = request.user.first_name
#             form.cleaned_data['address'] = user.addres
#             form.save()
#
