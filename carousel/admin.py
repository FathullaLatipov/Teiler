from django.contrib import admin

from carousel.models import CarouselModel


@admin.register(CarouselModel)
class CarouselModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'descriptions', 'created_at']
    search_fields = ['title']
    list_filter = ['title', 'created_at']
