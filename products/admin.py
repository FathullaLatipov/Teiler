from django.contrib import admin
from django.utils.safestring import mark_safe

from products.forms import ColorModelForm
from products.models import CategoryModel, ProductModel, ProductImageModel, BrandModel, ColorModel


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


class ProductImageModelAdmin(admin.TabularInline):
    model = ProductImageModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'sku', 'category', 'price', 'inbox', 'brand', 'material', 'created_at']
    list_filter = ['title', 'sku']
    search_fields = ['title', 'sku', 'category']
    autocomplete_fields = ['colors']
    inlines = [ProductImageModelAdmin]
    readonly_fields = ['real_price']
