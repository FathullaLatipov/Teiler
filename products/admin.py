from django.contrib import admin

from products.models import CategoryModel, ProductModel, ProductImageModel, BrandModel


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


class ProductImageModelAdmin(admin.TabularInline):
    model = ProductImageModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'sku', 'category', 'price', 'inbox', 'brand', 'material', 'created_at']
    list_filter = ['title', 'sku']
    search_fields = ['title', 'sku', 'category']
    inlines = [ProductImageModelAdmin]
    readonly_fields = ['real_price']
