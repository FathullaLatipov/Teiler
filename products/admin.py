from django.contrib import admin

from products.models import CategoryModel, ProductModel, ProductImageModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'created_at']
    list_filter = ['created_at']
    search_fields = ['category']


class ProductImageModelAdmin(admin.TabularInline):
    model = ProductImageModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'sku', 'category', 'price', 'inbox', 'brand', 'material', 'created_at']
    list_filter = ['title', 'sku']
    search_fields = ['title', 'sku', 'category']
    inlines = [ProductImageModelAdmin]


