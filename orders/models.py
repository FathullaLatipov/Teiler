from django.db import models

from products.models import ProductModel


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(OrderModel, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
