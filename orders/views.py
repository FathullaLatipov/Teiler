from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from coupons.forms import CouponApplyForm
from products.models import ProductModel
from user.models import CustomUser
from .models import OrderItem, OrderModel
from .forms import OrderCreateForm
from cart.cart import Cart
from .serializers import UserSerializer, OrderItemSerializer


@login_required(login_url="login")
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.phone = request.user.phone
            order.email = request.user.email
            order.user = request.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            coupon_apply_form = CouponApplyForm()
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order, 'coupon_apply_form': coupon_apply_form})

    else:
        form = OrderCreateForm()
        coupon_apply_form = CouponApplyForm()
        print("invalid")

    return render(request, 'orders/order/create.html',
                  {'form': form, 'cart': cart})


@login_required(login_url="signup")
def user_order_view(request, user_pk):
    user = CustomUser.objects.get(id=user_pk)
    user_orders = user.user_order.all()
    order_items = OrderItem.objects.select_related('product').filter(order__user_id=request.user)

    return render(request, 'lk.html', {'user_orders': user_orders,
                                       'order_items': order_items
                                       })


class UserAPIListView(ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="All infos user",
        operation_description="Methods for All infos user",
    )
    def list(self, request):
        queryset = OrderModel.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="GET user by ID(GET METHOD)",
        operation_description="Methods for GET user by ID(GET METHOD)",
    )
    def retrieve(self, request, pk=None):
        queryset = OrderModel.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="POST user (POST METHOD)",
        operation_description="Methods for POST user (POST METHOD)",
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_context(self):
        return {'request': self.request}


class OrderAPIListView(ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
# def create_order(request):
#     user = CustomUser
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             form.cleaned_data['first_name'] = request.user.first_name
#             # form.cleaned_data['address'] = user.addres
#             form.save()
#             print(form)
