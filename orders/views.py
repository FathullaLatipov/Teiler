from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from coupons.forms import CouponApplyForm
from products.models import ProductModel
from user.models import CustomUser
from .models import OrderItem, OrderModel
from .forms import OrderCreateForm
from cart.cart import Cart


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
            return render(request, 'orders/order/created.html', {'order': order, 'coupon_apply_form': coupon_apply_form})

    else:
        form = OrderCreateForm()
        coupon_apply_form = CouponApplyForm()

    return render(request, 'orders/order/create.html', {'form': form, 'cart': cart, 'coupon_apply_form': coupon_apply_form})


def user_order_view(request, user_pk):
    user = CustomUser.objects.get(id=user_pk)
    user_orders = user.user_order.all()
    order_items = OrderItem.objects.annotate(num_products=Sum('product'))
    print(order_items)

    return render(request, 'lk.html', {'user_orders': user_orders,
                                       'order_items': order_items
                                       })
