from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import ProductModel


class ReviewModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    email = models.EmailField(max_length=200, verbose_name=_('email'))
    comments = models.TextField()
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_('product'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
