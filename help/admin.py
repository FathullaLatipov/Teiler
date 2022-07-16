from django.contrib import admin

from help.models import HelpCategory, HelpSubcategory, HelpModel


@admin.register(HelpCategory)
class HelpCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']
    list_filter = ['title', 'created_at']


@admin.register(HelpSubcategory)
class HelpSubcategoryModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    search_fields = ['title']
    list_filter = ['title', 'created_at']


@admin.register(HelpModel)
class HelpModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    search_fields = ['title']
    list_filter = ['title', 'created_at']
