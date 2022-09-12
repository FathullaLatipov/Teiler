from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, Avg
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CategoryModel(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('title'))
    image = models.FileField(upload_to='image', verbose_name=_('image'), null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class SubCategoryModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, verbose_name=_('category'),
                                 related_name='subcategories')
    subcategory = models.CharField(max_length=100, verbose_name=_('subcategory'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subcategory

    class Meta:
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')


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
    subcategory = models.ForeignKey(SubCategoryModel, on_delete=models.CASCADE, verbose_name=_('subcategory'),
                                    null=True, )
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
    is_buy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def is_discount(self):
        return self.discount != 0

    def get_price(self):
        if self.is_discount():
            return self.price - self.price * self.discount / 100
        return self.price

    def grade(self):
        grade = ReviewModel.objects.filter(product=self, ).aggregate(avarage=Avg('rating'))
        avg = 0
        if grade["avarage"] is not None:
            avg = float(grade["avarage"])
        return avg

    @staticmethod
    def get_from_wishlist(request):
        wishlist = request.session.get('wishlist', [])
        return ProductModel.objects.filter(pk__in=wishlist)

    @staticmethod
    def get_from_cart(request):
        cart = request.session.get('cart', [])
        return ProductModel.objects.filter(pk__in=cart)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['title']


class ReviewModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    email = models.EmailField(max_length=200, verbose_name=_('email'))
    image = models.FileField(upload_to='form_images', verbose_name=_('image'), null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    comments = models.TextField()
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_('product'), related_name='rating')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'), null=True)

    def __str__(self):
        return self.name

    def rating_range(self):
        return range(1, self.rating + 1)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')


class ProductCustomNameModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='customer_names',
                                verbose_name=_('product'),
                                null=True, blank=True
                                )
    custom_name = models.CharField(max_length=200, verbose_name=_('custom_name'))
    custom_number = models.CharField(max_length=200, verbose_name=_('custom_number'))

    class Meta:
        verbose_name = _('product_custom_name')
        verbose_name_plural = _('product_custom_names')


class ProductCustomModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='customers',
                                verbose_name=_('product'), null=True, blank=True)

    custom = models.CharField(max_length=200, verbose_name=_('custom'))
    number = models.PositiveIntegerField(verbose_name=_('number'), null=True)
    price = models.PositiveIntegerField(verbose_name=_('price'), null=True)

    def __str__(self):
        return self.custom

    class Meta:
        verbose_name = _('product custom')
        verbose_name_plural = _('product customers')


class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='images',
                                verbose_name=_('product'), null=True, blank=True)

    image = models.FileField(upload_to='products', verbose_name=_('image'), null=True, blank=True)

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')


class ProductCharacteristicModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='characteristics',
                                verbose_name=_('product'), null=True, blank=True)

    data = models.CharField(max_length=300, verbose_name=_('data'))
    number = models.CharField(max_length=300, verbose_name=_('number'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('product_characteristic')
        verbose_name_plural = _('product_characteristics')


class RegisterForm(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True)
    phone = models.PositiveSmallIntegerField()
    password = models.CharField(max_length=100, null=True)
    confirm_password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('register')
        verbose_name_plural = _('registers')


class ProductAttributes(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_('product'))
    color = models.ForeignKey(ColorModel, on_delete=models.CASCADE,)
    num = models.ForeignKey(ProductCustomModel, on_delete=models.CASCADE,)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.product.title
