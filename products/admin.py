from django.contrib import admin
from django.utils.safestring import mark_safe
from products.forms import ColorModelForm
from products.models import CategoryModel, ProductModel, BrandModel, ColorModel, \
    ReviewModel, ProductCharacteristicModel, ProductImageModel, \
    ProductAttributes, ProductOptionsModel, ReviewImageModel, CurrentProductOptionsModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['category']


@admin.register(BrandModel)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'brand', 'created_at']
    list_filter = ['created_at']
    search_fields = ['brand']


@admin.register(ColorModel)
class ColorModelAdmin(admin.ModelAdmin):
    list_display = ['code', 'visual_color', 'created_at']
    search_fields = ['code']
    list_filter = ['created_at']
    form = ColorModelForm

    def visual_color(self, obj):
        return mark_safe(f'<div style="height: 20px; width: 100px; background: {obj.code}"></div>')


@admin.register(ReviewImageModel)
class ReviewImageModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'image', 'created_at']


@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'comments', 'email', 'created_at']


class ProductImageModelAdmin(admin.TabularInline):
    model = ProductImageModel


class CurrentProductOptionsModelAdmin(admin.TabularInline):
    model = CurrentProductOptionsModel
    extra = 1


class ProductOptionsModelAdmin(admin.TabularInline):
    model = ProductOptionsModel


class ProductCharacteristicModelAdmin(admin.TabularInline):
    model = ProductCharacteristicModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'sku', 'category', 'price', 'inbox', 'brand', 'material', 'created_at']
    list_filter = ['title', 'sku']
    search_fields = ['title', 'sku']
    autocomplete_fields = ['сolors']
    inlines = [ProductImageModelAdmin, CurrentProductOptionsModelAdmin, ProductOptionsModelAdmin,
               ProductCharacteristicModelAdmin]
    readonly_fields = ['real_price']
    save_as = True
    save_on_top = True


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'option_title', 'option_number']


admin.site.register(ProductAttributes, ProductAttributeAdmin)
