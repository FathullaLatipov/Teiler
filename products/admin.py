from django.contrib import admin
from django.utils.safestring import mark_safe
from products.forms import ColorModelForm
from products.models import CategoryModel, ProductModel, ProductCustomModel, BrandModel, ColorModel, \
    ReviewModel, ProductCharacteristicModel, SubCategoryModel, ProductImageModel, ProductCustomNameModel, \
    ProductAttributes


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['category']


@admin.register(SubCategoryModel)
class SubCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category', 'subcategory', 'created_at']
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


@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'comments', 'email', 'created_at']


class ProductCustomNameModelAdmin(admin.TabularInline):
    model = ProductCustomNameModel
    extra = 1


class ProductCustomModelAdmin(admin.TabularInline):
    model = ProductCustomModel

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        if db_field.name == 'YOUR_FIELD_NAME':
            kwargs['choices'] = (('', '---------'), ('1', 'Choice1'), ('2', 'Choice2'))
        return db_field.formfield(**kwargs)


class ProductImageModelAdmin(admin.TabularInline):
    model = ProductImageModel


class ProductCharacteristicModelAdmin(admin.TabularInline):
    model = ProductCharacteristicModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'sku', 'category', 'price', 'inbox', 'brand', 'material', 'created_at']
    list_filter = ['title', 'sku']
    search_fields = ['title', 'sku']
    autocomplete_fields = ['colors']
    inlines = [ProductCustomNameModelAdmin, ProductCustomModelAdmin, ProductImageModelAdmin,
               ProductCharacteristicModelAdmin]
    readonly_fields = ['real_price']
    save_as = True
    save_on_top = True


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'price', 'color', 'num']


admin.site.register(ProductAttributes, ProductAttributeAdmin)
