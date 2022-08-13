from django.shortcuts import render
from django.views.generic import ListView

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
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})

    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'form': form, 'cart': cart})


def user_order_view(request, user_pk):
    user = CustomUser.objects.get(id=user_pk)
    user_orders = user.user_order.all()

    # for item in user_orders.order_items.all():
    #     print(item)
    return render(request, 'lk.html', {'user_orders': user_orders})
