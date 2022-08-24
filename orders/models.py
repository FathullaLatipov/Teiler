from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from coupons.models import Coupon
from products.models import ProductModel
from user.models import CustomUser


class OrderModel(models.Model):
    first_name = models.CharField(max_length=50,null=True, blank=True)
    last_name = models.CharField(max_length=50,null=True, blank=True)
    phone = models.PositiveIntegerField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    Online_choices = (
        ("online", "Картой онлайн"),
        ("chache", "Оплата при получении"),
    )
    online = models.CharField(
        max_length=50,
        choices=Online_choices,
        null=True,
        blank=True
    )

    Receiving_choices = (
        ("email", "Получить почтой"),
        ("deliver", "Доставить курьером"),
        ("ru_mail", "Получить из почтамата"),
    )

    upon_receipt = models.CharField(
        max_length=200,
        choices=Receiving_choices,
        null=True,
        blank=True
    )

    Order_choices = (
        ("process", "В процессе"),
        ("cancel", "Заказ отменен"),
        ("delivery", "Выполняется доставка"),
        ("success", "Товар получен"),
    )

    status = models.CharField(
        max_length=200,
        choices=Order_choices,
        null=True,
        default="process",
        blank=True
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='user_order')
    address = models.CharField(max_length=100, verbose_name='address', null=True)
    flat_office = models.CharField(max_length=100, verbose_name='flat_office', null=True)
    entrance = models.CharField(max_length=100, verbose_name='entrance', null=True)
    intercom = models.CharField(max_length=100, verbose_name='intercom', null=True)
    floor = models.CharField(max_length=100, verbose_name='floor', null=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(OrderModel, related_name='order', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
