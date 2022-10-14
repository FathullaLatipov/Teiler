from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, Avg
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CategoryModel(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('title'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    image = models.FileField(upload_to='image', verbose_name=_('image'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['pk']


class BrandModel(models.Model):
    brand = models.CharField(max_length=99, verbose_name=_('brands'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')


class ColorModel(models.Model):
    color_title = models.CharField(max_length=100, verbose_name=_('title'), null=True)
    code = models.CharField(max_length=10, verbose_name=_('code'))
    color_type = models.CharField(default='color', max_length=20, null=True)
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
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, verbose_name=_('category'),
                                 related_name='cat_price')
    image = models.FileField(upload_to='image', verbose_name=_('image'), null=True)
    price = models.IntegerField(verbose_name=_('price'))
    discount = models.DecimalField(default=0, max_digits=9, decimal_places=0, verbose_name=_('discount'))
    promotional_price = models.CharField(max_length=200, verbose_name=_('promotional_price'))
    inbox = models.CharField(max_length=300, verbose_name=_('inbox'))
    description = models.TextField(verbose_name=_('description'), null=True)
    material = models.CharField(max_length=300, verbose_name=_('material'))
    country = models.CharField(max_length=300, verbose_name=_('country'))
    сolors = models.ManyToManyField(
        ColorModel,
        related_name='products',
        verbose_name=_('colors')
    )
    season = models.CharField(max_length=200, verbose_name=_('season'))
    real_price = models.FloatField(verbose_name=_('real price'), default=0)
    is_published = models.BooleanField(default=False)
    is_buy = models.BooleanField(default=False)
    is_fav = models.BooleanField(default=False)
    Condition_choices = (
        ("NEW", 'Новый'),
        ("USED", 'Б/у')
    )
    condition = models.CharField(
        max_length=20,
        verbose_name=_('condition'),
        choices=Condition_choices,
        null=True,
        blank=True
    )
    Order_choices = (
        ("process", "В процессе"),
        ("canceled", "Отменен"),
        ("wait_send", "Ожидает доставка"),
        ("wait_rev", "Ожидает отзыв"),
        ("complete", "Товар получен"),
    )

    status = models.CharField(
        max_length=200,
        choices=Order_choices,
        null=True,
        default="process",
        blank=True
    )
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
    name = models.CharField(max_length=100, verbose_name=_('name'), null=True, blank=True)
    email = models.EmailField(max_length=200, verbose_name=_('email'), null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    comments = models.TextField()
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_('product'),
                                related_name='rating')
    review_count = models.IntegerField(default=0, )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'), null=True)

    def __str__(self):
        return self.name

    def rating_range(self):
        return range(1, self.rating + 1)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        ordering = ['pk']


class ReviewImageModel(models.Model):
    image = models.ImageField(upload_to='form_images', verbose_name=_('image'), null=True, blank=True, )
    review = models.ForeignKey(ReviewModel, on_delete=models.CASCADE, null=True, related_name='images')

    class Meta:
        verbose_name = _('review_image')
        verbose_name_plural = _('reviews_image')


class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='images',
                                verbose_name=_('product'), null=True, blank=True)

    image = models.FileField(upload_to='products', verbose_name=_('image'), null=True, blank=True)

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')


class ProductOptionsModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='products_options',
                                verbose_name=_('product'), null=True, blank=True)

    options_title = models.CharField(max_length=300, verbose_name=_('options_title'))
    options_number = models.CharField(max_length=300, verbose_name=_('options_number'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('product_options')
        verbose_name_plural = _('product_options')


class ProductCharacteristicModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='characteristics',
                                verbose_name=_('product'), null=True, blank=True)

    chars_title = models.CharField(max_length=300, verbose_name=_('data'))
    chars_number = models.CharField(max_length=300, verbose_name=_('number'))
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
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_('product'),
                                related_name='product_options')
    option_title = models.CharField(max_length=300, verbose_name=_('option_title'), null=True)
    option_number = models.CharField(max_length=900, verbose_name=_('option_number'), null=True)
    option_type = models.CharField(max_length=90, default='default', null=True, blank=True)

    def __str__(self):
        return self.product.title
