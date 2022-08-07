from django.contrib.auth import user_logged_in
from django.db.models.signals import pre_save
from django.dispatch import receiver

from products.models import ProductModel, BasketModel


@receiver(pre_save, sender=ProductModel)
def real_price_calc(sender, instance, *args, **kwargs):
    if instance.is_discount():
        instance.real_price = instance.price - instance.price * instance.discount / 100
    else:
        instance.real_price = instance.price


@receiver(user_logged_in)
def merge_basket_if_found(sender, user, request, **kwargs):
    anonymous_basket = getattr(request, "basket", None)
    if anonymous_basket:
        try:
            loggedin_basket = BasketModel.objects.get(
                user=user
            )
            for line in anonymous_basket.basketline_set.all():
                line.basket = loggedin_basket
                line.save()
            anonymous_basket.delete()
            request.basket = loggedin_basket

        except BasketModel.DoesNotExist:
            anonymous_basket.user = user
            anonymous_basket.save()

