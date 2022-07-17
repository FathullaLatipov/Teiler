from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from star_ratings.models import Rating


class CategoryModel(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('title'))
    image = models.FileField(upload_to='image', verbose_name=_('image'), null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class BrandModel(models.Model):
    brand = models.CharField(max_length=99, verbose_name=_('brands'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')


class ColorModel(models.Model):
    code = models.CharField(max_length=10, verbose_name=_('code'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')


# Товар: имя, код, бренд, категория,
# количество, цена, акционная цена, наличии или не в наличии,
# описание, материал, страна производитель, сезон, цвет,
# количество просмотров, много картин,

class ProductModel(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('title'), db_index=True)
    sku = models.IntegerField(verbose_name=_('sku'), db_index=True)
    brand = models.ForeignKey(BrandModel, on_delete=models.PROTECT, verbose_name=_('brand'))
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, verbose_name=_('category'))
    image = models.FileField(upload_to='image', verbose_name=_('image'), null=True)
    price = models.IntegerField(verbose_name=_('price'))
    discount = models.DecimalField(default=0, max_digits=9, decimal_places=0, verbose_name=_('discount'))
    promotional_price = models.CharField(max_length=200, verbose_name=_('promotional_price'))
    inbox = models.CharField(max_length=300, verbose_name=_('inbox'))
    description = RichTextUploadingField(verbose_name=_('description'), null=True)
    material = models.CharField(max_length=300, verbose_name=_('material'))
    country = models.CharField(max_length=300, verbose_name=_('country'))
    colors = models.ManyToManyField(
        ColorModel,
        related_name='products',
        verbose_name=_('colors')
    )
    season = models.CharField(max_length=200, verbose_name=_('season'))
    real_price = models.FloatField(verbose_name=_('real price'), default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def is_discount(self):
        return self.discount != 0

    def get_price(self):
        if self.is_discount():
            return self.price - self.price * self.discount / 100
        return self.price

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['title']


class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='product',
                                verbose_name=_('product'), null=True, blank=True)

    image = models.FileField(upload_to='products', verbose_name=_('image'), null=True, blank=True)

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')
