from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
import logging

from products import exceptions

logger = logging.getLogger(__name__)


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
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name=_('product'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'), null=True)

    def __str__(self):
        return self.name

    def rating_range(self):
        return range(1, self.rating + 1)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("StarRating", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "star_rating"
        verbose_name_plural = "star_ratings"
        ordering = ["-value"]


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


class BasketModel(models.Model):
    OPEN = 10
    SUBMITTED = 20
    STATUSES = ((OPEN, "Open"), (SUBMITTED, "Submitted"))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )

    status = models.IntegerField(choices=STATUSES, default=OPEN)

    def is_empty(self):
        return self.basketline_set.all().count() == 0

    def count(self):
        return sum(i.quantity for i in self.basketline_set.all())

    def create_order(self, billing_address, shipping_address):
        if not self.user:
            raise exceptions.BasketException(
                "Cannot create order without user"
            )
        logger.info(
            "Creating order for basket_id=%d"",shipping_address_id=%d,billing_address_id=%d",
            self.pk,
            shipping_address.pk,
            billing_address.pk,
        )

        order_data = {
            "user": self.user,
            "billing_name": billing_address.name,
            "billing_address1": billing_address.address1,
            "billing_address2": billing_address.address2,
            "billing_zip_code": billing_address.zip_code,
            "billing_city": billing_address.city,
            "billing_country": billing_address.country,
            "shipping_name": shipping_address.name,
            "shipping_address1": shipping_address.address1,
            "shipping_address2": shipping_address.address2,
            "shipping_zip_code": shipping_address.zip_code,
            "shipping_city": shipping_address.city,
            "shipping_country": shipping_address.country,
        }

        order = OrderModel.objects.create(**order_data)
        c = 0
        for line in self.basketline_set.all():
            for item in range(line.quantity):
                order_line_data = {
                    "order": order,
                    "product": line.product,
                }
                order_line = OrderLine.objects.create(
                    **order_line_data
                )
                c += 1
        logger.info(
            "Created order with id=%d and lines_count=%d", order.pk, c,
        )

        self.status = BasketModel.SUBMITTED
        self.save()
        return order


class AddressModel(models.Model):

    SUPPORTED_COUNTRIES = (
        ("uk", "United Kingdom"),
        ("us", "United States of America"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=60)
    address1 = models.CharField("Address line 1", max_length=60)
    address2 = models.CharField(
        "Address line 2", max_length=60, blank=True
    )
    zip_code = models.CharField(
        "ZIP / Postal code", max_length=12
    )
    city = models.CharField(max_length=60)
    country = models.CharField(
        max_length=3, choices=SUPPORTED_COUNTRIES
    )

    def __str__(self):
        return ", ".join(
            [
                self.name,
                self.address1,
                self.address2,
                self.zip_code,
                self.city,
                self.country,
            ]
        )


class BasketLine(models.Model):
    basket = models.ForeignKey(BasketModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


class OrderModel(models.Model):
    NEW = 10
    PAID = 20
    DONE = 30
    CANCELLED = 40
    STATUS = (
        (NEW, "New"),
        (PAID, "Paid"),
        (DONE, "Done"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    status = models.IntegerField(choices=STATUS, default=NEW)

    billing_name = models.CharField(max_length=60)
    billing_address1 = models.CharField(max_length=60)
    billing_address2 = models.CharField(max_length=60, blank=True)
    billing_zip_code = models.CharField(max_length=12)
    billing_city = models.CharField(max_length=60)
    billing_country = models.CharField(max_length=4)

    shipping_name = models.CharField(max_length=60)
    shipping_address1 = models.CharField(max_length=60)
    shipping_address2 = models.CharField(max_length=60, blank=True)

    shipping_zip_code = models.CharField(max_length=20)
    shipping_city = models.CharField(max_length=60)
    shipping_country = models.CharField(max_length=60)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderLine(models.Model):
    NEW = 10
    PROCESSING = 20
    SENT = 30
    CANCELLED = 40
    STATUS = (
        (NEW, "New"),
        (PROCESSING, "Processing"),
        (SENT, "Sent"),
        (CANCELLED, 'Cancelled')
    )
    order = models.ForeignKey(
        OrderModel, on_delete=models.CASCADE, related_name="lines"
    )
    product = models.ForeignKey(
        ProductModel, on_delete=models.PROTECT
    )
    status = models.IntegerField(choices=STATUS, default=NEW)
